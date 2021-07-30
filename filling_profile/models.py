import datetime

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import CASCADE


class Profile(models.Model):
    full_name = models.CharField('полнейшее имя', max_length=50, blank=True)
    email = models.CharField('email адрес', max_length=50, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    skills = models.CharField('навыки', max_length=150, null=True)
    goal = models.IntegerField('цель общенщения', default=None, null=True, blank=True)
    contacts = models.CharField('Telegram', max_length=15, default=[''], null=True, blank=True)
    language = models.CharField('язык', max_length=20, default='', null=True, blank=True)
    meeting_status = models.CharField(max_length=20, default="not ready", null=True)

    def __str__(self):
        return self.full_name


class Skills(models.Model):
    skill_id = models.AutoField(primary_key=True)
    skill_title = models.CharField(max_length=50)
    skill_category = models.CharField(max_length=50, default='')

    def __str__(self):
        return f'{self.skill_category}: {self.skill_title}'


class Categories(models.Model):
    skill_id = models.AutoField(primary_key=True)
    category_title = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.category_title}'


class Profile_for_Metting(models.Model):
    profile = models.ForeignKey(Profile, on_delete=CASCADE, blank=True)


class Meet(models.Model):
    id = models.AutoField(primary_key=True)
    first_profile = models.ForeignKey(Profile, on_delete=CASCADE, related_name='first_profile_id', blank=True)
    second_profile = models.ForeignKey(Profile, on_delete=CASCADE, related_name='second_profile_id', blank=True)
    meet_id = models.CharField(max_length=10, null=True)
    date_meeting = models.DateField(default=datetime.datetime.now(), null=True)
    feedback = models.CharField(max_length=10, null=True)
    goal_id = models.CharField(max_length=10, null=True)
