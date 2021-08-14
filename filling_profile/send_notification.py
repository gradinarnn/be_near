



import json
from filling_profile.models import Profile
import requests
import be_near.constants


def send_MEET_notification(first_profile_id,second_profile_id):

    user_id_first = Profile.objects.get(id=first_profile_id).contacts
    user_id_second = Profile.objects.get(id=second_profile_id).contacts
    
    # узнаем usename второго пользователя, чтобы отправить первому
    url = f"https://api.telegram.org/bot{be_near.constants.bot_token}/getChatMember?user_id={user_id_second}&chat_id={user_id_second}"

    payload={}
    headers = {}

    username = requests.request("POST", url, headers=headers, data=payload).json().get("result").get("user").get("username")
    

    # отправляем сообщение первому пользователю
    text = f'Мы нашли тебе себеседника @{username}'

    url = f'https://api.telegram.org/bot{be_near.constants.bot_token}/sendMessage?chat_id={user_id_first}&text={text}'

    payload={}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)



    


    

    # узнаем usename второго пользователя
    url = f"https://api.telegram.org/bot{be_near.constants.bot_token}/getChatMember?user_id={user_id_first}&chat_id={user_id_first}"

    payload={}
    headers = {}

    username = requests.request("POST", url, headers=headers, data=payload).json().get("result").get("user").get("username")
    

    # отправляем сообщение второму пользователю
    text = f'Мы нашли тебе себеседника @{username}'

    url = f'https://api.telegram.org/bot{be_near.constants.bot_token}/sendMessage?chat_id={user_id_second}&text={text}'

    payload={}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

 