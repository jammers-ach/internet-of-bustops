# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 07:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0011_player_last_checkin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='in_progress',
            field=models.BooleanField(default=True),
        ),
    ]