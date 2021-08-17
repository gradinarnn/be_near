# Generated by Django 3.2.6 on 2021-08-17 14:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filling_profile', '0003_auto_20210817_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meet',
            name='date_meeting',
            field=models.DateField(default=datetime.datetime(2021, 8, 17, 17, 27, 43, 332281), null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='email адрес'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=models.CharField(max_length=150, null=True, verbose_name='навыки'),
        ),
    ]
