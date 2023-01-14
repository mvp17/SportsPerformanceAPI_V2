from django.contrib import admin
from app.models.LoadData import LoadData
from app.models.ConfigurationSetting import ConfigurationSetting
from app.models.KeyWordEventsFile import KeyWordEventsFile
from app.models.KeyWordDevicesFile import KeyWordDevicesFile


admin.site.register(LoadData)
admin.site.register(ConfigurationSetting)
admin.site.register(KeyWordEventsFile)
admin.site.register(KeyWordDevicesFile)
