# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-10 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rescueapp', '0019_added_viasms_bool'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='DateFinished',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='incident',
            name='IncidentType',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]