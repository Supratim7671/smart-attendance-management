# Generated by Django 2.0.1 on 2018-01-26 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='fbranchid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='faculty.branch'),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='fsubjectid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='faculty.subject'),
        ),
    ]