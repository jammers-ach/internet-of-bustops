# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-26 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0002_auto_20161126_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensordata',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]