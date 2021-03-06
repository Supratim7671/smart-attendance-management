# Generated by Django 2.0.1 on 2018-01-25 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='attendance',
            fields=[
                ('aid', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now=True)),
                ('period', models.IntegerField(default=0)),
                ('modeofclass', models.CharField(default='L', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='attendancerecord',
            fields=[
                ('rid', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default='', max_length=500)),
                ('aid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.attendance')),
            ],
        ),
        migrations.CreateModel(
            name='branch',
            fields=[
                ('branchid', models.AutoField(primary_key=True, serialize=False)),
                ('branchname', models.CharField(default='', max_length=500)),
                ('year', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(default='', max_length=500)),
                ('fpost', models.CharField(default=0, max_length=200)),
                ('fmobile', models.IntegerField(default=0)),
                ('faddress', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='staffs',
            fields=[
                ('staffid', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(default='', max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('role', models.CharField(default='admin', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sname', models.CharField(default='', max_length=500)),
                ('smobile', models.IntegerField(default=0)),
                ('saddress', models.CharField(default='', max_length=500)),
                ('sbranchid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.branch')),
            ],
        ),
        migrations.CreateModel(
            name='subject',
            fields=[
                ('subjectid', models.AutoField(primary_key=True, serialize=False)),
                ('subjectname', models.CharField(default='', max_length=500)),
                ('branchid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.branch')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='ssubjectid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.subject'),
        ),
        migrations.AddField(
            model_name='student',
            name='studentid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.staffs'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='facultyid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.staffs'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='fbranchid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.branch'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='fsubjectid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.subject'),
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='studentid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.staffs'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='asbranchid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.branch'),
        ),
    ]
