from django.db import models

from datetime import datetime, timedelta
from django.db.models import CASCADE

import filling_profile


class Ten_Minutes_Profile_List(models.Model):
    profile = models.ForeignKey(filling_profile.models.Profile, on_delete=CASCADE)

    def __str__(self):
        return self.profile.full_name

    class Meta:
        db_table = 'Ten_Minutes_Profile_List'



class Ten_Minutes_Meet(models.Model):
    id = models.AutoField(primary_key=True)
    first_profile_id = models.CharField(max_length=20, blank=True)
    second_profile_id = models.CharField(max_length=20, blank=True)
    date_meeting = models.DateField(default=datetime.now(), null=True)
    status = models.CharField(max_length=10, null=True)
    first_feedback = models.CharField(max_length=10, blank=True, null=True)
    second_feedback = models.CharField(max_length=10, blank=True, null=True)


    class Meta:
        db_table = 'Ten_Minutes_Meet'

    def __str__(self):
        first_profile = Ten_Minutes_Profile_List.objects.get(id=self.first_profile_id).full_name
        second_profile = Ten_Minutes_Profile_List.objects.get(id=self.second_profile_id).full_name

        return str(f'{self.id}. {first_profile} & {second_profile}. Status: {self.status}')