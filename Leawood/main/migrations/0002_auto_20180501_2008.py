# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-01 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data_log_entry',
            old_name='metadata',
            new_name='param_metadata',
        ),
        migrations.AlterField(
            model_name='property_metadata',
            name='data_type',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
