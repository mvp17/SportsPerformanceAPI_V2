import pandas as pd
from app.forms.SettingsForm import SettingsForm
from app.models.LoadData import LoadData
from app.models.KeyWordEventsFile import KeyWordEventsFile
from app.models.KeyWordDevicesFile import KeyWordDevicesFile
from django.contrib import messages
from django.shortcuts import render, redirect
from app.utils import is_there_events_file_uploaded,  \
                      is_there_devices_file_uploaded, \
                      remove_accent,                  \
                      process_device_data,            \
                      process_event_data,             \
                      get_events_csv_dict,            \
                      get_init_time_and_fin_time


def configuration(request):
    # If no csv files uploaded, error message.
    # If no key words entered, while there are files uploaded of each type, error message.

    objects_data = LoadData.objects.all()

    if LoadData.objects.count() == 0:
        messages.error(request, 'Error: No data to analyse. Please upload some csv files.')
        return render(request, 'settings.html')
    elif KeyWordEventsFile.objects.count() == 0 and is_there_events_file_uploaded(objects_data):
        messages.error(request, 'Error: No events file key words known, although there is events file uploaded.')
        return render(request, 'settings.html')
    elif KeyWordDevicesFile.objects.count() == 0 and is_there_devices_file_uploaded(objects_data):
        messages.error(request, 'Error: No devices file/s key words known, although there is devices file/s uploaded.')
        return render(request, 'settings.html')
    else:
        objects_data = LoadData.objects.all()
        context_init_time = 0
        context_fin_time = 0
        time_ms_name_events_file = ""
        duration_time_ms_name_events_file = ""
        time_name_devices_file = ""
        if KeyWordEventsFile.objects.count() == 1:
            time_ms_name_events_file = KeyWordEventsFile.load().time_ms_name
            duration_time_ms_name_events_file = KeyWordEventsFile.load().duration_time_ms_name
        if KeyWordDevicesFile.objects.count() == 1:
            time_name_devices_file = KeyWordDevicesFile.load().time_name

        for obj in objects_data:
            remove_accent(obj.csv.name)
            csv = pd.read_csv(obj.csv.name)
            performance_variables = csv.columns.values.tolist()
            data = {}

            for perf_var in performance_variables:
                data[perf_var.replace(" ", "_")] = []

            if obj.event_file == 0:
                for row in csv.values.tolist():
                    for (element_row, perf_var) in zip(row, performance_variables):
                        data[perf_var.replace(" ", "_")].append(element_row)
                file_dict = process_event_data(data, obj.frequency, time_ms_name_events_file,
                                               duration_time_ms_name_events_file)
                context_init_time, context_fin_time = get_init_time_and_fin_time(file_dict, time_ms_name_events_file)
            else:
                for row in csv.values.tolist():
                    for (element_row, perf_var) in zip(row, performance_variables):
                        data[perf_var.replace(" ", "_")].append(element_row)

                if is_there_events_file_uploaded(objects_data):
                    events_csv_dict = get_events_csv_dict(objects_data)
                    value = events_csv_dict.get(time_ms_name_events_file)[0]
                    file_dict = process_device_data(data, value, obj.frequency, time_name_devices_file)
                    context_init_time, context_fin_time = get_init_time_and_fin_time(file_dict, time_name_devices_file)
                else:
                    file_dict = process_device_data(data, 0, obj.frequency, time_name_devices_file)
                    context_init_time, context_fin_time = get_init_time_and_fin_time(file_dict, time_name_devices_file)

    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SettingsForm()

    if context_init_time == 0 and context_fin_time == 0:
        messages.error(request, 'Error in fetching filtering initial time and final time')

    return render(request, 'settings.html', {
        'form': form, 'init_time': context_init_time, 'fin_time': context_fin_time
    })
