# Generated by Django 3.2.6 on 2021-08-30 12:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filling_profile', '0006_auto_20210830_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meet',
            name='date_meeting',
            field=models.DateField(default=datetime.datetime(2021, 8, 30, 15, 5, 25, 501745), null=True),
        ),
        migrations.AlterField(
            model_name='meet',
            name='goal_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
