# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-07 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rescueapp', '0016_added_after_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='MiddleName',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
