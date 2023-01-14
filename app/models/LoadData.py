from django.db import models


class LoadData(models.Model):
    title = models.CharField(max_length=100, blank=True)
    athlete = models.CharField(max_length=100, blank=True)
    csv = models.FileField(upload_to='csv_files/')

    CHOICES_BOOL = [(0, "Yes"), (1, "No")]
    event_file = models.IntegerField(blank=False, help_text="Is it events file what you are uploading?",
                                     choices=CHOICES_BOOL, default=0)

    FREQ_1FS = 1
    FREQ_5FS = 5
    FREQ_10FS = 10
    FREQ_25FS = 25
    FREQ_100FS = 100
    FREQ_1000FS = 1000
    FREQ_NONE = 0
    FREQ_CHOICES = [(FREQ_NONE, ""),
                    (FREQ_1FS, "1 Hz"),
                    (FREQ_5FS, "5 Hz"),
                    (FREQ_10FS, "10 Hz"),
                    (FREQ_25FS, "25 Hz"),
                    (FREQ_100FS, "100 Hz"),
                    (FREQ_1000FS, "1000 Hz")
                    ]
    frequency = models.IntegerField(choices=FREQ_CHOICES, default=FREQ_NONE,
                                    help_text="Ignore the field when uploading EVENTS file.")

    def delete(self, *args, **kwargs):
        self.csv.delete()
        super().delete(*args, **kwargs)
