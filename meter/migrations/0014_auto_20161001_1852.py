# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-01 17:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meter', '0013_auto_20161001_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='currency',
            field=models.CharField(choices=[('euro', 'euro'), ('$', 'us dollar')], default='euro', max_length=6),
        ),
    ]