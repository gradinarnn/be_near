# Generated by Django 3.2.6 on 2021-09-02 09:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ten_minutes_meet', '0002_auto_20210901_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ten_minutes_meet',
            name='date_meeting',
            field=models.DateField(default=datetime.datetime(2021, 9, 2, 12, 52, 30, 555657), null=True),
        ),
    ]
