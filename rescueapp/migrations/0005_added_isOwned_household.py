# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-26 06:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rescueapp', '0004_evacenter_assoc_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='household',
            name='IsOwned',
            field=models.BooleanField(default=True),
        ),
    ]
