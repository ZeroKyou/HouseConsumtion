from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


# Create your models here.
class Electricity(models.Model):
    ''' Model for the energy '''

    current = models.FloatField()
    voltage = models.FloatField(default=230.0)
    date = models.DateTimeField(default=timezone.now)

    @property
    def power(self):
        return self.voltage * self.current

    def __str__(self):
        return "Current: {0}, Voltage: {1}, Power: {2}\n".format(self.current, self.voltage, self.power)