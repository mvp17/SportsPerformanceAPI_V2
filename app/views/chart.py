from app.models import *
from django.contrib import messages
from django.shortcuts import render
from app.utils import *
import json


def chart(request):
    objects_data = LoadData.objects.all()
    if not is_there_events_file_uploaded(objects_data):
        messages.error(request, 'Error: No events file uploaded.')
        return render(request, 'chart.html')
    elif KeyWordEventsFile.objects.count() == 0 and is_there_events_file_uploaded(objects_data):
        messages.error(request, 'Error: No events file key words known, although there is events file uploaded.')
        return render(request, 'chart.html')
    else:
        lists_labels, lists_data, chart_vars = get_info_chart(objects_data)
        lists_labels = to_format_csv(lists_labels)

        return render(request, 'chart.html', {
            "lists_data": json.dumps(lists_data), "lists_labels": json.dumps(lists_labels), "chart_vars": chart_vars
        })


# Data of which perf variables as key words for events file
def get_info_chart(objects_data):
    events_data = get_events_csv_dict(objects_data)
    chart_perf_vars = ""
    duration_time_name_events_ms = ""

    if KeyWordEventsFile.objects.count() == 1 and is_there_events_file_uploaded(objects_data):
        chart_perf_vars = KeyWordEventsFile.load().chart_perf_vars
        duration_time_name_events_ms = KeyWordEventsFile.load().duration_time_ms_name

    float_data_to_int_data(events_data, duration_time_name_events_ms)

    # Worst case
    chart_perf_vars = chart_perf_vars.replace(" ", "")
    perf_vars_list = chart_perf_vars.split(",")
    sub_events = {}

    for key in events_data.keys():
        if key in perf_vars_list:
            sub_events[key] = events_data[key]

    list_labels_with_their_data = get_data_and_labels(sub_events.values())
    lists_labels, lists_data = split_labels_data(list_labels_with_their_data)

    return lists_labels, lists_data, perf_vars_list


def get_data_and_labels(values):
    list_different_values = {}
    list_labels_data = []

    for element in values:
        for value in element:
            if value not in list_different_values:
                # Don't count with the NaN values
                if isinstance(value, float) and math.isnan(value):
                    continue
                list_different_values[value] = 1
            else:
                list_different_values[value] += 1
        list_labels_data.append(list_different_values)
        list_different_values = {}

    return list_labels_data


def split_labels_data(list_labels_with_their_data):
    lists_labels = []
    lists_data = []
    list_labels = []
    list_data = []

    for element in list_labels_with_their_data:

        for key in element.keys():
            list_labels.append(key)
        lists_labels.append(list_labels)
        list_labels = []

        for value in element.values():
            list_data.append(value)
        lists_data.append(list_data)
        list_data = []

    return lists_labels, lists_data


def to_format_csv(lists_labels):
    new_lists_labels = []
    new_list_labels = []

    for list_label in lists_labels:
        for label in list_label:
            if isinstance(label, str):
                if ',' in label:
                    label = label.replace(',', '.')
                    new_list_labels.append(label)
                else:
                    new_list_labels.append(label)
            else:
                new_list_labels.append(label)
        new_lists_labels.append(new_list_labels)
        new_list_labels = []
    return new_lists_labels
