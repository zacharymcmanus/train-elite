# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-29 07:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_quote'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Quote',
        ),
    ]
