from django.db import models
from app.models.Singleton import Singleton


class ConfigurationSetting(Singleton):
    init_time_ms = models.PositiveIntegerField(null=True, blank=False, help_text="Time in milliseconds.")
    fin_time_ms = models.PositiveIntegerField(null=True, blank=False, help_text="Time in milliseconds.")

    FREQ_1FS = 1
    FREQ_5FS = 5
    FREQ_10FS = 10
    FREQ_25FS = 25
    FREQ_100FS = 100
    FREQ_1000FS = 1000
    FREQ_CHOICES = [(FREQ_1FS, "1 Hz"),
                    (FREQ_5FS, "5 Hz"),
                    (FREQ_10FS, "10 Hz"),
                    (FREQ_25FS, "25 Hz"),
                    (FREQ_100FS, "100 Hz"),
                    (FREQ_1000FS, "1000 Hz")
                    ]
    frequency = models.IntegerField(choices=FREQ_CHOICES, default=FREQ_5FS, help_text="Data table frequency.")
