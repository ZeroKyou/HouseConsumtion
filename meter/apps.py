from __future__ import unicode_literals
from django.apps import AppConfig


class MeterConfig(AppConfig):
    name = 'meter'

    def ready(self):
        import meter.signals
