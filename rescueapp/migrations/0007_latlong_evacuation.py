# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-29 04:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rescueapp', '0006_household_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='evacuationcenter',
            name='Latitude',
            field=models.DecimalField(decimal_places=8, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='evacuationcenter',
            name='Longitude',
            field=models.DecimalField(decimal_places=8, max_digits=8, null=True),
        ),
    ]
