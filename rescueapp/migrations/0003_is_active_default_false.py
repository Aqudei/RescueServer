# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 01:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rescueapp', '0002_is_active_default_true'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='IsActive',
            field=models.BooleanField(default=False),
        ),
    ]