from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from meter.managers import ElectricityManager, WaterManager


class Electricity(models.Model):
    '''
    Model for storing current, voltage and power readings
    and the date they've reached the server.
    '''

    current = models.FloatField()
    voltage = models.FloatField(default=230.0)
    date = models.DateTimeField(default=timezone.now)

    objects = ElectricityManager()

    @property
    def power(self):
        return self.voltage * self.current

    def __str__(self):
        return "Current: {0}, Voltage: {1}, Power: {2}, Date: {3}\n".format(
            self.current,
            self.voltage,
            self.power,
            self.date)


class Water(models.Model):
    '''
    Model for storing number of liters of water read, and the date
    they've reached the server.
    '''
    liters = models.FloatField()
    date = models.DateTimeField(default=timezone.now)

    objects = WaterManager()

    def __str__(self):
        return "Liters: {0}, Date: {1}\n".format(self.liters, self.date)


class Settings(models.Model):
    '''
    Model that represents each user's website settings
    '''

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)
    cost_kw_per_hour = models.FloatField(default=0.19, null=False)
    cost_liter = models.FloatField(default=0.9, null=False)
    power_warning = models.FloatField()
    water_liters_warning = models.FloatField()
    send_email = models.BooleanField(default=False)

    def __str__(self):
        return """User: {0}, Electricity Cost(kW/h): {1}, Water Cost(l): {2}, Send email: {3}, Power Warning: {4},
         Water Liters Warning; {5}\n""".format(
            self.user.username,
            self.cost_kw_per_hour,
            self.cost_liter,
            self.send_email,
            self.power_warning,
            self.water_liters_warning)
