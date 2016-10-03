from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Electricity(models.Model):
    '''
    Model for storing current, voltage and power readings
    and the date they reached the server.
    '''

    current = models.FloatField()
    voltage = models.FloatField(default=230.0)
    date = models.DateTimeField(default=timezone.now)

    @property
    def power(self):
        return self.voltage * self.current

    def __str__(self):
        return "Current: {0}, Voltage: {1}, Power: {2}\n".format(
            self.current,
            self.voltage,
            self.power)


class Settings(models.Model):
    '''
    Model that represents each user's website settings
    '''

    CURRENCY_OPTIONS = (
        ("eur", "euro"),
        ("usd", "us dollar"))

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)
    cost_kw_per_hour = models.FloatField(default=None, null=True)
    send_email = models.BooleanField(default=False)
    currency = models.CharField(
        max_length=6,
        choices=CURRENCY_OPTIONS,
        default="eur"
    )

    def __str__(self):
        return "User: {0}, Cost(kW/h): {1}, Send email: {2}, Currency: {3}\n".format(
            self.user.username,
            self.cost_kw_per_hour,
            self.send_email,
            self.currency)
