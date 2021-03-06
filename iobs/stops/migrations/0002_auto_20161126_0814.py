# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-26 08:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_progress', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('pos', models.IntegerField(choices=[(0, 'up'), (1, 'left')])),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('playing', models.BooleanField(default=True)),
                ('bus_stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stops.BusStop')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stops.Game')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='turn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_turn', to='stops.Player'),
        ),
    ]
