import schedule
import time

import schedule
from filling_profile.models import Profile
import requests


def send_message(bot_token, user_id, text):
    telegram_id = get_telegram_id(user_id)
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={telegram_id}&text={text}'

    payload = {}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)


def get_username(bot_token, user_id):
    telegram_id = get_telegram_id(user_id)

    url = f"https://api.telegram.org/bot{bot_token}/getChatMember?user_id={telegram_id}&chat_id={telegram_id}"
    payload = {}
    headers = {}
    return requests.request("POST", url, headers=headers, data=payload).json().get("result").get("user").get(
        "username")


def get_telegram_id(user_id):
    print(f'*******user_id в get_telegram_id{user_id}')
    return Profile.objects.get(id=user_id).contacts
