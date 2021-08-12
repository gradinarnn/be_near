# Generated by Django 3.2.6 on 2021-08-12 11:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(blank=True, max_length=50, verbose_name='полнейшее имя')),
                ('email', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='email адрес')),
                ('skills', models.CharField(max_length=150, null=True, verbose_name='навыки')),
                ('goal', models.IntegerField(blank=True, default=None, null=True, verbose_name='цель общенщения')),
                ('contacts', models.CharField(blank=True, default=[''], max_length=15, null=True, verbose_name='Telegram')),
                ('language', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='язык')),
                ('meeting_status', models.CharField(default='not ready', max_length=20, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'Profile',
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('skill_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_title', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('skill_id', models.AutoField(primary_key=True, serialize=False)),
                ('skill_title', models.CharField(max_length=50)),
                ('skill_category', models.CharField(default='', max_length=50)),
            ],
            options={
                'db_table': 'Skills',
            },
        ),
        migrations.CreateModel(
            name='Profile_for_Metting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Profile_for_Metting',
            },
        ),
        migrations.CreateModel(
            name='Meet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('meet_id', models.CharField(max_length=10, null=True)),
                ('date_meeting', models.DateField(default=datetime.datetime(2021, 8, 12, 14, 44, 4, 481591), null=True)),
                ('feedback', models.CharField(max_length=10, null=True)),
                ('goal_id', models.CharField(max_length=10, null=True)),
                ('first_profile', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='first_profile_id', to=settings.AUTH_USER_MODEL)),
                ('second_profile', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='second_profile_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Meet',
            },
        ),
    ]