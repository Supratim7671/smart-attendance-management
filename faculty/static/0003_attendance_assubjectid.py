# Generated by Django 2.0.1 on 2018-01-27 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0002_auto_20180127_0124'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='assubjectid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='faculty.subject'),
        ),
    ]
