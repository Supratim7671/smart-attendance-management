# Generated by Django 2.0.1 on 2018-03-05 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0003_attendance_assubjectid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faculty',
            name='fsubjectid',
        ),
    ]
