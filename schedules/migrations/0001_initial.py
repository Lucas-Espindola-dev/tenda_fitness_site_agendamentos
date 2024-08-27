# Generated by Django 5.0.6 on 2024-07-17 19:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('day', models.DateField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('repeat', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('time', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='schedules.time')),
            ],
            options={
                'unique_together': {('day', 'time')},
            },
        ),
    ]
