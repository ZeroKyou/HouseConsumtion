# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import EmailMessage
from meter.models import Settings


def values():
    '''
    Stores the values of the electrical power and liters of water
    to be compared against the value of the ones in
    each user's settings. If these values are greater, an email will be sent
    to those users.
    Ex: values.to_send = {'Electricity': 24, 'Water': 8}
    '''
    values.to_send = {}
values()


@receiver(post_save, sender=User)
def create_settings(sender, created, instance, **kwargs):
    '''
    Creates a new Settings object, associated to the new user
    and saves it to the database.
    '''
    if created:
        settings = Settings.create_settings(user=instance)
        settings.save()


@receiver(post_save)
def send_email(sender, created, instance, **kwargs):
    '''
    Sends emails to all the users whose consumption limits have been exceeded
    by the last electricity and water readings.
    '''
    sender_models = ['Electricity', 'Water']
    data_type = {'Electricity': 'power', 'Water': 'water_liters'}
    if sender.__name__ in sender_models:
        if created:
            if len(values.to_send) == 0:
                values.to_send[data_type[sender.__name__]] = instance.get_reading()
            else:
                values.to_send[data_type[sender.__name__]] = instance.get_reading()
                emails = Settings.objects.send_email(values.to_send)
                if len(emails) > 0:
                    email_message = EmailMessage('Limite de consumo excedido',
                                                 """Limite de água ou eletricidade excedidos:
                                                  Potência: {0}, Litros de água: {1}""".format(
                                                    values.to_send['power'], values.to_send['water_liters']),
                                                 to=emails)
                    email_message.send()
                values.to_send = {}
