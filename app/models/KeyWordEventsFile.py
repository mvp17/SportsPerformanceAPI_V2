from django.db import models
from app.models.Singleton import Singleton


class KeyWordEventsFile(Singleton):
    time_ms_name = models.CharField(null=True, max_length=100, blank=False,
                                    help_text="Column name of Time in milli-seconds values.")
    duration_time_ms_name = models.CharField(null=True, max_length=100, blank=False,
                                             help_text="Column name of Time Duration in milli-seconds values.")
    chart_perf_vars = models.TextField(blank=True, max_length=250,
                                       help_text="Performance variables separated by comma for showing their data "
                                                 "to the chart data. Use white spaces if you like. "
                                                 "Please put the variables in the same order as they are shown."
                                       )
