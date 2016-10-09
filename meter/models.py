# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core import validators
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

    @property
    def cubic_meters(self):
        return round(self.liters / 1000, 3);

    def __str__(self):
        return "Liters: {0}, Cubic Meters: {1}, Date: {2}\n".format(self.liters, self.cubic_meters, self.date)


class Settings(models.Model):
    '''
    Model that represents each user's website settings
    '''
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)
    cost_kw_per_hour = models.FloatField(default=0.19,
                                         null=False,
                                         blank=False,
                                         validators=[validators.MinValueValidator(
                                                 0.0, "Custo da eletricidade tem de ser positivo")]
                                         )
    cost_m3 = models.FloatField(default=0.9,
                                null=False,
                                blank=False,
                                validators=[validators.MinValueValidator(
                                    0.0, "Custo da água tem de ser positivo")]
                                )
    power_warning = models.FloatField(default=0.0,
                                      null=False,
                                      blank=False,
                                      validators=[validators.MinValueValidator(
                                          0.0, "Limite de consumo elétrico tem de ser positivo")]
                                      )
    liters_warning = models.FloatField(default=0.0,
                                       null=False,
                                       blank=False,
                                       validators=[validators.MinValueValidator(
                                                 0.0, "Limite de consumo de água tem de ser positivo")]
                                       )
    send_email = models.BooleanField(default=False)

    @classmethod
    def create_settings(cls, user):
        settings = cls(user=user)
        return settings

    def __str__(self):
        return """User: {0}, Electricity Cost(kW/h): {1}, Water Cost(l): {2}, Send email: {3}, Power Warning: {4},
         Water Liters Warning: {5}\n""".format(
            self.user.username,
            self.cost_kw_per_hour,
            self.cost_m3,
            self.send_email,
            self.power_warning,
            self.liters_warning)
