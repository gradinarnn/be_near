import json

import requests

from be_near.constants import host
from filling_profile.models import Profile, Profile_for_Metting


def change_meeting_status(user_id, status):
    token_value = Profile.objects.get(id=user_id).token
    payload_data = {"meeting_status": status}
    payload_dict = {"profile": payload_data}
    payload = json.dumps(payload_dict)

    url = host + "/filling_profile/user/"
    token = 'Bearer ' + token_value
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    response = requests.request("PATCH", url, headers=headers, data=payload)

    if status == "meetting":
        profile=Profile_for_Metting.objects.get(profile=Profile.objects.get(id=user_id))
        profile.delete()