# Generated by Django 2.0.1 on 2018-03-25 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0003_faculty_fbranchid'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='sbranchid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='faculty.branch'),
        ),
    ]