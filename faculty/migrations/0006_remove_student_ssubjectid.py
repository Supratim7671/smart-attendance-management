# Generated by Django 2.0.1 on 2018-03-25 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0005_student_ssubjectid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='ssubjectid',
        ),
    ]
