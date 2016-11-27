# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 06:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0010_merge_20161126_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='last_checkin',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.datetime_safe.datetime.now),
            preserve_default=False,
        ),
    ]
