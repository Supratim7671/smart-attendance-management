# Generated by Django 2.0.1 on 2018-03-25 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0006_remove_student_ssubjectid'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='ssubjectid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='faculty.subject'),
        ),
    ]