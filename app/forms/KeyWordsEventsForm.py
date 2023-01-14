from django import forms
from app.models.KeyWordEventsFile import *


class KeyWordsEventsForm(forms.ModelForm):
    class Meta:
        model = KeyWordEventsFile
        fields = ('time_ms_name', 'duration_time_ms_name', 'chart_perf_vars')