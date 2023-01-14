from app.models import *
from django.shortcuts import render, redirect


def exit_session(request):
    is_there_configuration = 0
    if KeyWordEventsFile.objects.count() == 1 or KeyWordDevicesFile.objects.count() == 1 or \
            ConfigurationSetting.objects.count() == 1:
        is_there_configuration = 1
    return render(request, 'exit.html', {
        "is_there_configuration": is_there_configuration
    })


def delete_session(request):
    KeyWordEventsFile.load().delete()
    KeyWordDevicesFile.load().delete()
    ConfigurationSetting.load().delete()

    return redirect('exit')
