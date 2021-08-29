import be_near.constants
import requests
from filling_profile.models import Profile




# Возвращает username пользователя по его id в БД
def username_from_id(id):
    profile = Profile.objects.get(id = id).contacts
    url = f"https://api.telegram.org/bot{be_near.constants.bot_token}/getChatMember?user_id={profile}&chat_id={profile}"

    payload={}
    headers = {}

    return requests.request("POST", url, headers=headers, data=payload).json().get("result").get("user").get("username")