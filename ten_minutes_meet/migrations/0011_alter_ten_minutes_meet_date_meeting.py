# Generated by Django 3.2.6 on 2021-09-07 09:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ten_minutes_meet', '0010_alter_ten_minutes_meet_date_meeting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ten_minutes_meet',
            name='date_meeting',
            field=models.DateField(default=datetime.datetime(2021, 9, 7, 12, 54, 54, 567646), null=True),
        ),
    ]
