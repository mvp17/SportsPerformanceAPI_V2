from app.models import *
from django.contrib import messages
from django.shortcuts import render
from app.utils import *
import json


def data_analytics(request):
    # If no csv files uploaded, error message.
    # If no settings configured, error message.
    # If no key words of events file entered, error message.
    # If no key words of devices file/s entered, error message.

    objects_data = LoadData.objects.all()

    if LoadData.objects.count() == 0:
        messages.error(request, 'Error: No data to analyse. Please upload some csv files.')
        return render(request, 'data_analytics.html')
    elif KeyWordEventsFile.objects.count() == 0 and is_there_events_file_uploaded(objects_data):
        messages.error(request, 'Error: No events file key words known, although there is events file uploaded.')
        return render(request, 'data_analytics.html')
    elif KeyWordDevicesFile.objects.count() == 0 and is_there_devices_file_uploaded(objects_data):
        messages.error(request, 'Error: No devices file/s key words known, although there is devices file/s uploaded.')
        return render(request, 'data_analytics.html')
    elif ConfigurationSetting.objects.count() == 0:
        messages.error(request, 'Error: No settings configured. Please go to Settings and enter your configuration.')
        return render(request, 'data_analytics.html')
    else:
        frequency_data_table = ConfigurationSetting.load().frequency
        init_time = ConfigurationSetting.load().init_time_ms
        fin_time = ConfigurationSetting.load().fin_time_ms
        time_ms_name_events_file = ""
        duration_time_ms_name_events_file = ""
        time_name_devices_file = ""
        if KeyWordEventsFile.objects.count() == 1 and is_there_events_file_uploaded(objects_data):
            time_ms_name_events_file = KeyWordEventsFile.load().time_ms_name
            duration_time_ms_name_events_file = KeyWordEventsFile.load().duration_time_ms_name
        if KeyWordDevicesFile.objects.count() == 1 and is_there_devices_file_uploaded(objects_data):
            time_name_devices_file = KeyWordDevicesFile.load().time_name
        dict_devices = []
        dict_down_sampled_files = []

        for obj in objects_data:
            data = {}
            remove_accent(obj.csv.name)
            csv = pd.read_csv(obj.csv.name, ";")
            performance_variables = csv.columns.values.tolist()

            for perf_var in performance_variables:
                data[perf_var.replace(" ", "_")] = []

            if obj.event_file == 0:
                for row in csv.values.tolist():
                    for (element_row, element_perf_var) in zip(row, performance_variables):
                        data[element_perf_var.replace(" ", "_")].append(element_row)
                event_file_dict = process_event_data(data, obj.frequency,
                                                     time_ms_name_events_file, duration_time_ms_name_events_file)
                file_init_time, file_fin_time = get_init_time_and_fin_time(event_file_dict, time_ms_name_events_file)

                if not (fin_time <= file_fin_time and init_time >= file_init_time):
                    messages.error(request, 'Error: It is not possible to analyse data '
                                            'with the settings time parameters. Please re-enter the '
                                            'settings time parameters.')
                    return render(request, 'data_analytics.html')

                dict_down_sampled_files.append(swap_columns(down_sample(event_file_dict, frequency_data_table,
                                                                        time_ms_name_events_file,
                                                                        time_name_devices_file),
                                                            time_ms_name_events_file))
            else:
                for row in csv.values.tolist():
                    for (element_row, element_perf_var) in zip(row, performance_variables):
                        data[element_perf_var.replace(" ", "_")].append(element_row)
                if is_there_events_file_uploaded(objects_data):
                    events_csv_dict = get_events_csv_dict(objects_data)
                    value = events_csv_dict.get(time_ms_name_events_file)[0]
                    dict_devices.append(process_device_data(data, value, obj.frequency, time_name_devices_file))
                else:
                    dict_devices.append(process_device_data(data, 0, obj.frequency, time_name_devices_file))

        for device_data in dict_devices:
            file_init_time, file_fin_time = get_init_time_and_fin_time(device_data, time_name_devices_file)

            if not (fin_time <= file_fin_time and init_time >= file_init_time):
                messages.error(request, 'Error: It is not possible to analyse data '
                                        'with the settings time parameters. Please re-enter the '
                                        'settings time parameters.')
                return render(request, 'data_analytics.html')

            dict_down_sampled_files.append(down_sample(device_data, frequency_data_table, time_ms_name_events_file,
                                                       time_name_devices_file))

        render_data_files = filter_time_files(dict_down_sampled_files,
                                              ConfigurationSetting.load().init_time_ms,
                                              ConfigurationSetting.load().fin_time_ms, time_ms_name_events_file,
                                              duration_time_ms_name_events_file, time_name_devices_file)
        for file in render_data_files:
            for value in file.values():
                for element in value:
                    if isinstance(element, float) and math.isnan(element):
                        value[value.index(element)] = 'null'

        vars_perf = []
        for file in render_data_files:
            for key in file.keys():
                if key not in vars_perf:
                    vars_perf.append(key)

        context = {'perf_vars_list': vars_perf, 'dict_csv_files': json.dumps(render_data_files)}
        return render(request, 'data_analytics.html', context)


def filter_time_files(dict_down_sampled_files, init_filter_time, fin_filter_time, events_time_name,
                      events_duration_time_name, devices_time_name):
    files_to_render = []
    for file in dict_down_sampled_files:
        df = pd.DataFrame.from_dict(file, orient="columns")
        df.to_csv("filtered_time_files.csv")
        csv = pd.read_csv("filtered_time_files.csv", header=0, index_col=[0])
        os.remove("filtered_time_files.csv")
        performance_variables = csv.columns.values.tolist()
        data = {}
        for var in performance_variables:
            data[var] = []
        for row in csv.values.tolist():
            filter_time = False
            for (element_row, element_perf_var) in zip(row, performance_variables):
                if element_perf_var == events_time_name or element_perf_var == devices_time_name:
                    if fin_filter_time >= element_row >= init_filter_time:
                        filter_time = True
                        data[element_perf_var].append(element_row)
                else:
                    if filter_time:
                        data[element_perf_var].append(element_row)
        float_data_to_int_data(data, events_duration_time_name)
        files_to_render.append(data)
    return files_to_render


def down_sample(dict_csv, table_frequency, events_time_name, devices_time_name):
    # Frequency of dict_csv data is 1000 Hz
    if table_frequency != 1000:
        average = int(round(1000/table_frequency))
        time = []
        for key in dict_csv.keys():
            downsampled = dict_csv.get(key)[0::average]
            if key == events_time_name or key == devices_time_name:
                for element in downsampled:
                    time.append(round(element / 10) * 10)
                dict_csv[key] = time
            else:
                dict_csv[key] = downsampled
            dict_csv[key] = downsampled
    return dict_csv


def remove_accent(feed):
    csv_f = open(feed, encoding='latin-1', mode='r')
    csv_str = csv_f.read()
    csv_str_removed_accent = unidecode.unidecode(csv_str)
    csv_f.close()
    csv_f = open(feed, 'w')
    csv_f.write(csv_str_removed_accent)


def swap_columns(old_dict, time_name):
    # In the EVENTS file put the time in milliseconds column in the first place of the csv,
    # in order to do the time filter well.
    new_dict = {}

    for key in old_dict.keys():
        if key == time_name:
            new_dict[key] = old_dict[key]
            del old_dict[key]
            break

    for key in old_dict.keys():
        new_dict[key] = old_dict[key]

    return new_dict
