from django import forms
from app.models.LoadData import *


class FileForm(forms.ModelForm):
    class Meta:
        model = LoadData
        fields = ('title', 'athlete', 'csv', 'event_file', 'frequency')
