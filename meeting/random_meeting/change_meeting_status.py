import json

import requests

from be_near.constants import host, not_ready_status_constant, meeting_status_constant
from filling_profile.models import Profile, Profile_for_Metting


def change_meeting_status(user_id, status):
    profile = Profile.objects.get(id=user_id)
    profile.meeting_status = status
    profile.save()

    if (status == meeting_status_constant) or (status == not_ready_status_constant):
        try:
            profile_for_meeting=Profile_for_Metting.objects.get(profile=Profile.objects.get(id=user_id))
            profile_for_meeting.delete()
        except Profile_for_Metting.DoesNotExist:
            print('Профиля нет в таблице')
