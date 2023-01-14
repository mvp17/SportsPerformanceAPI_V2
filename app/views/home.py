
from app.models import *
from django.shortcuts import render


def home(request):
    init_time = 0
    fin_time = 0
    frequency = 0
    is_there_configuration = 0
    is_there_key_words_events = 0
    is_there_key_words_devices = 0
    is_there_chart_perf_vars = 0
    time_ms_name_events = ""
    duration_time_ms_name_events = ""
    chart_perf_vars = ""
    time_name_devices = ""
    if ConfigurationSetting.objects.count() == 1:
        is_there_configuration = 1
        frequency = ConfigurationSetting.load().frequency
        init_time = ConfigurationSetting.load().init_time_ms
        fin_time = ConfigurationSetting.load().fin_time_ms
    if KeyWordEventsFile.objects.count() == 1:
        is_there_key_words_events = 1
        time_ms_name_events = KeyWordEventsFile.load().time_ms_name
        duration_time_ms_name_events = KeyWordEventsFile.load().duration_time_ms_name
        if KeyWordEventsFile.load().chart_perf_vars is None or not KeyWordEventsFile.load().chart_perf_vars:
            is_there_chart_perf_vars = 1
        else:
            chart_perf_vars = KeyWordEventsFile.load().chart_perf_vars
    if KeyWordDevicesFile.objects.count() == 1:
        is_there_key_words_devices = 1
        time_name_devices = KeyWordDevicesFile.load().time_name

    return render(request, 'base.html', {
        'init_time': init_time, 'fin_time': fin_time, 'frequency': frequency,
        'is_there_configuration': is_there_configuration, 'time_ms_name_events': time_ms_name_events,
        'duration_time_ms_name_events': duration_time_ms_name_events, 'chart_perf_vars': chart_perf_vars,
        'time_name_devices': time_name_devices, 'is_there_key_words_events': is_there_key_words_events,
        'is_there_key_words_devices': is_there_key_words_devices,
        'is_there_chart_perf_vars': is_there_chart_perf_vars
    })
