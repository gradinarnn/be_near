
import schedule
import time
from aiogram.utils.callback_data import CallbackData
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import schedule
import json
from filling_profile.models import Profile
import requests
import be_near.constants


def send_MEET_notification(first_profile_id,second_profile_id,text1,text2):

    user_id_first = Profile.objects.get(id=first_profile_id).contacts
    user_id_second = Profile.objects.get(id=second_profile_id).contacts

    print(f'***********user_id_first:{user_id_first}')
    print(f'***********user_id_second:{user_id_second}')
    
    # узнаем usename второго пользователя, чтобы отправить первому
    url = f"https://api.telegram.org/bot{be_near.constants.bot_token}/getChatMember?user_id={user_id_second}&chat_id={user_id_second}"

    payload={}
    headers = {}

    username = requests.request("POST", url, headers=headers, data=payload).json().get("result").get("user").get("username")

    print(f'***********username2:{username}')
    

    # отправляем сообщение первому пользователю
    text = text1+f' @{username}'

    url = f'https://api.telegram.org/bot{be_near.constants.bot_token}/sendMessage?chat_id={user_id_first}&text={text}'

    payload={}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)


    # узнаем usename первого пользователя, чтобы отправить второму
    url = f"https://api.telegram.org/bot{be_near.constants.bot_token}/getChatMember?user_id={user_id_first}&chat_id={user_id_first}"

    payload={}
    headers = {}

    username = requests.request("POST", url, headers=headers, data=payload).json().get("result").get("user").get("username")

    print(f'***********username1:{username}')
    

    # отправляем сообщение первому пользователю
    text = text2 + f' @{username}'

    url = f'https://api.telegram.org/bot{be_near.constants.bot_token}/sendMessage?chat_id={user_id_second}&text={text}'

    payload={}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)











 