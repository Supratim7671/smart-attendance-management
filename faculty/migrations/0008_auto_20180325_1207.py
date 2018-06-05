# Generated by Django 2.0.1 on 2018-03-25 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0007_student_ssubjectid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='ssubjectid',
        ),
        migrations.AddField(
            model_name='student',
            name='ssubjectid',
            field=models.ManyToManyField(default='', null=True, to='faculty.subject'),
        ),
    ]
