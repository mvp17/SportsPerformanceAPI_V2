from django import forms
from app.models.ConfigurationSetting import *


class SettingsForm(forms.ModelForm):
    class Meta:
        model = ConfigurationSetting
        fields = ('init_time_ms', 'fin_time_ms', 'frequency')