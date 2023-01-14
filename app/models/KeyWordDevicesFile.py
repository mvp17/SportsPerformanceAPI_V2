from django.db import models
from app.models.Singleton import Singleton


class KeyWordDevicesFile(Singleton):
    time_name = models.CharField(null=True, max_length=100, blank=False,
                                 help_text="Column name of Time of DEVICES files.")
