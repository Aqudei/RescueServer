# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 22:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rescueapp', '0018_change_to_checkin_monitoring'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='ViaSMS',
            field=models.BooleanField(default=False),
        ),
    ]
