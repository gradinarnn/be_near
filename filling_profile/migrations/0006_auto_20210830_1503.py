# Generated by Django 3.2.6 on 2021-08-30 12:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filling_profile', '0005_auto_20210830_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meet',
            name='date_meeting',
            field=models.DateField(default=datetime.datetime(2021, 8, 30, 15, 3, 11, 410969), null=True),
        ),
        migrations.AlterField(
            model_name='meet',
            name='second_feedback',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='meet',
            name='second_profile_id',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
