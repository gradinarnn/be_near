# Generated by Django 3.2.6 on 2021-08-12 13:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filling_profile', '0006_alter_meet_date_meeting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meet',
            name='date_meeting',
            field=models.DateField(default=datetime.datetime(2021, 8, 12, 16, 55, 41, 884931), null=True),
        ),
    ]
