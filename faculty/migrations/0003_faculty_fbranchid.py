# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-05 15:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0002_auto_20180305_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='fbranchid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='faculty.branch'),
        ),
    ]
