from django import forms
from app.models.KeyWordDevicesFile import *


class KeyWordsDevicesForm(forms.ModelForm):
    class Meta:
        model = KeyWordDevicesFile
        fields = ('time_name',)