# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-16 19:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0011_auto_20181015_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='creator',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='maker', to='first_app.User'),
            preserve_default=False,
        ),
    ]