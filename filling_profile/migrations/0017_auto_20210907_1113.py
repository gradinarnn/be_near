# Generated by Django 3.2.6 on 2021-09-07 08:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filling_profile', '0016_alter_meet_date_meeting'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categories',
            old_name='skill_id',
            new_name='category_id',
        ),
        migrations.RemoveField(
            model_name='skills',
            name='skill_category',
        ),
        migrations.AddField(
            model_name='skills',
            name='category',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='filling_profile.categories'),
        ),
        migrations.AlterField(
            model_name='meet',
            name='date_meeting',
            field=models.DateField(default=datetime.datetime(2021, 9, 7, 11, 13, 54, 402498), null=True),
        ),
    ]
