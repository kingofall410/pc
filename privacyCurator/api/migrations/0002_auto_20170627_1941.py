# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 23:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='startTime',
            field=models.DateTimeField(),
        ),
    ]