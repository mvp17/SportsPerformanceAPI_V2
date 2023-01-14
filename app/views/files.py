from app.forms.KeyWordsEventsForm import KeyWordsEventsForm
from app.forms.KeyWordsDevicesForm import KeyWordsDevicesForm
from app.forms.FileForm import FileForm
from django.views.generic import ListView
from app.models.LoadData import LoadData
from django.contrib import messages
from django.shortcuts import render, redirect
from app.utils import is_there_events_file_uploaded, is_there_devices_file_uploaded, remove_accent
import pandas as pd


def delete_file(request, pk):
    if request.method == 'POST':
        file = LoadData.objects.get(pk=pk)
        file.delete()
    return redirect('file_list')


class FileList(ListView):
    model = LoadData
    template_name = 'uploading/file_list.html'
    context_object_name = 'files'


def set_key_words_events_file(request):
    # If no csv files uploaded, error message.
    if LoadData.objects.count() == 0:
        messages.error(request, 'Error: No data to analyse. Please upload some csv files.')
        return render(request, 'uploading/set_key_words.html')
    else:
        context_perf_vars = set_key_words(0, request)

    if request.method == 'POST':
        form = KeyWordsEventsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = KeyWordsEventsForm()

    return render(request, 'uploading/set_key_words.html', {
        'form': form, 'perf_vars': context_perf_vars
    })


def set_key_words_devices_file(request):
    # If no csv files uploaded, error message.
    if LoadData.objects.count() == 0:
        messages.error(request, 'Error: No data to analyse. Please upload some csv files.')
        return render(request, 'uploading/set_key_words.html')
    else:
        context_perf_vars = set_key_words(1, request)

    if request.method == 'POST':
        form = KeyWordsDevicesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = KeyWordsDevicesForm()
    return render(request, 'uploading/set_key_words.html', {
        'form': form, 'perf_vars': context_perf_vars
    })


def set_key_words(is_events_or_devices_file, request):
    objects_data = LoadData.objects.all()
    context_perf_vars = []

    if is_there_devices_file_uploaded(objects_data) and is_events_or_devices_file == 0 \
            and not is_there_events_file_uploaded(objects_data):
        messages.error(request, 'Error. There are not events files uploaded.')
    elif is_there_events_file_uploaded(objects_data) and is_events_or_devices_file == 1 \
            and not is_there_devices_file_uploaded(objects_data):
        messages.error(request, 'Error. There are not devices files uploaded')
    else:
        for obj in objects_data:
            if obj.event_file == is_events_or_devices_file:
                remove_accent(obj.csv.name)
                csv = pd.read_csv(obj.csv.name, ";")
                performance_variables = csv.columns.values.tolist()
                for perf_var in performance_variables:
                    perf_var = perf_var.replace(" ", "_")
                    if perf_var not in context_perf_vars:
                        context_perf_vars.append(perf_var)

    return context_perf_vars


def upload_csv_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        csv_file = request.FILES['csv']
        if form.is_valid() and csv_file.name.endswith('.csv'):
            form.save()
            return redirect('file_list')
        else:
            messages.error(request, 'Error in parameters. Should upload only csv files.')
    else:
        form = FileForm()
    return render(request, 'uploading/upload_file.html', {
        'form': form
    })
