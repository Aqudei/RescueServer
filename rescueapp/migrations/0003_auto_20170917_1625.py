# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-17 08:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rescueapp', '0002_auto_20170917_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]
