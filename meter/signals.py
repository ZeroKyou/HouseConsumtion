from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from meter.models import Settings


@receiver(post_save, sender=User)
def create_settings(sender, created, instance, **kwargs):
    if created:
        settings = Settings.create_settings(user=instance)
        settings.save()
