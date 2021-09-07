from sched import scheduler

from django.db.models import Q

import be_near.constants
import json
import random
from be_near.constants import host, main_bot_token
from filling_profile.CallbackData import checking_meeting, meeting_feedback

import threading
import schedule
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from filling_profile.models import Profile, Profile_for_Metting, Meet
import requests
import time

import jwt
import requests

from telegram_services.send_message import get_telegram_id, get_username
from telegram_services.send_message import send_message

"""  Запустить процес формирования встреч  """

def meeting():
    all_profiles = Profile_for_Metting.objects.all()

    while len(all_profiles) > 0:
        print(f'-------------Весь список до взятия первого: {all_profiles}---------------------')
        all_profiles = list(all_profiles)
        print(f'-------------all_profiles list: {all_profiles}---------------------')
        first_profile = all_profiles.pop(0)
        print(f'-------------Первый пользователь: {first_profile.profile_id}---------------------')
        print(f'-------------Весь список после взятия первого: {all_profiles}---------------------')

        selection_list = all_profiles.copy()

        meeting_success = False
        while (len(selection_list) > 0) and (not meeting_success):
            second_profile_number = random.randint(0, len(selection_list) - 1)
            second_profile = selection_list.pop(second_profile_number)
            print(f'-------------Второй пользователь: {second_profile.profile_id}-------------------')
            print(f'-------------Весь список после взятия второго: {all_profiles}---------------------')
            print(f'-------------Cписок в котором ищется второй: {selection_list}---------------------')

            # if ..... проверка встречались ли first_profile и second_profile до этого

            meeting_list = list(Meet.objects.all().filter(first_profile_id=first_profile.profile_id)) + list(
                Meet.objects.all().filter(second_profile_id=first_profile.profile_id))

            print(f'-------------Список в котором {first_profile} есть: {meeting_list}---------------------')

            meeting_indicator = False
            for meet in meeting_list:

                if (second_profile.profile_id == meet.first_profile_id) or (
                        second_profile.profile_id == meet.second_profile_id):
                    meeting_indicator = True
                    print(
                        f'-------------meeting_indicator = {meeting_indicator}. А весь список при этом: {all_profiles}')

            print(f'-------------meeting_indicator: {meeting_indicator}---------------------')
            if not meeting_indicator:
                print(f'------------Пара сформирована--------------')
                meeting = Meet(first_profile_id=first_profile.profile_id, second_profile_id=second_profile.profile_id,
                               status='active')
                print(f'----meeting:{meeting}--------------')
                meeting.save()

                send_message(bot_token=main_bot_token, user_id=first_profile.profile_id,
                             text=f'Мы нашли тебе себеседника @{get_username(bot_token=main_bot_token, user_id=second_profile.profile_id)}. Ему интересно: {second_profile.profile.skills}.Приятной встречи 🌱')

                send_message(bot_token=main_bot_token, user_id=second_profile.profile_id,
                             text=f'Мы нашли тебе себеседника @{get_username(bot_token=main_bot_token, user_id=first_profile.profile_id)}. Ему интересно: {first_profile.profile.skills}.Приятной встречи 🌱')

                # меняем статус встречи первого пользователя на "meeting"
                token_value = Profile.objects.get(id=first_profile.profile_id).token
                payload_data = {"meeting_status": "meetting"}
                payload_dict = {"profile": payload_data}
                payload = json.dumps(payload_dict)

                url = host + "/filling_profile/user/"
                token = 'Bearer ' + token_value
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }
                response = requests.request("PATCH", url, headers=headers, data=payload)

                # меняем статус встречи второго пользователя на "meeting"
                token_value = Profile.objects.get(id=second_profile.profile_id).token
                payload_data = {"meeting_status": "meetting"}
                payload_dict = {"profile": payload_data}
                payload = json.dumps(payload_dict)

                url = host + "/filling_profile/user/"
                token = 'Bearer ' + token_value
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }
                response = requests.request("PATCH", url, headers=headers, data=payload)

                meeting_success = True
            else:

                print(f'------------Такая пара уже была--------------')
                print(f'-------------А весь список при этом: {all_profiles}---------------------')

        if meeting_success == True:
            print(f'-------------Удаляем пользователя: {all_profiles[second_profile_number]}---------------------')
            all_profiles.pop(second_profile_number)


"""  Проверка в среду, удалось ли связаться с собеседником  """

def check_meeting_3_day():
    text = f'🙌 Привет! Уже узпел паобщаться с собеседником?'
    buttons = InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Да, всё гуд',
                    callback_data=checking_meeting.new(status="ok_good!"),

                ),
                InlineKeyboardButton(
                    text='Нет, ещё не общались',
                    callback_data=checking_meeting.new(status="not_communicate")

                ),
                InlineKeyboardButton(
                    text='Парнёр не отвечает',
                    callback_data=checking_meeting.new(status="not_answer")

                )
            ]
        ]
    )

    all_active_meets = Meet.objects.all().filter(status='active')

    for meets in all_active_meets:

        # Если профиль был удален кем-то и как-то, то это предотвратит ошибку
        try:
            first_profile = Profile.objects.get(id=meets.first_profile_id).contacts
            profile = True
        except Profile.DoesNotExist:
            profile = False
        if profile:
            url = f'https://api.telegram.org/bot{main_bot_token}/sendMessage?chat_id={first_profile}&text={text}&reply_markup={buttons}'

            payload = {}
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload)
        profile = False
        try:
            second_profile = Profile.objects.get(id=meets.second_profile_id).contacts
            profile = True
        except Profile.DoesNotExist:
            profile = False
        if profile:
            url = f'https://api.telegram.org/bot{main_bot_token}/sendMessage?chat_id={second_profile}&text={text}&reply_markup={buttons}'
            response = requests.request("POST", url, headers=headers, data=payload)


"""  В воскресенье отправляем сообщение для оценки встречи  """

def every_saturday():
    all_active_meets = Meet.objects.all().filter(status='active')
    buttons = InlineKeyboardMarkup(
        row_width=5,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='👎',
                    callback_data=meeting_feedback.new(status="1")

                ),
                InlineKeyboardButton(
                    text='😒',
                    callback_data=meeting_feedback.new(status="2")

                ),
                InlineKeyboardButton(
                    text='🙂',
                    callback_data=meeting_feedback.new(status="3")

                ),

                InlineKeyboardButton(
                    text='😍',
                    callback_data=meeting_feedback.new(status="4")
                ),
                InlineKeyboardButton(
                    text='👍',
                    callback_data=meeting_feedback.new(status="5")
                )

            ]
        ]
    )
    print(f'**********all_active_meets из every_saturday:{all_active_meets}')
    for meet in all_active_meets:
        # Если профиль был удален кем-то и как-то, то это предотвратит ошибку
        try:
            first_profile = Profile.objects.get(id=meet.first_profile_id).contacts
            profile = True
        except Profile.DoesNotExist:
            profile = False
        if profile:
            print(f'**********meet.second_profile_id из every_saturday:{meet.second_profile_id}')
            text = f'✨ Хэй, как прошла встреча с @{get_username(main_bot_token, meet.second_profile_id)}? Можешь оценить встречу?'
            url = f'https://api.telegram.org/bot{main_bot_token}/sendMessage?chat_id={first_profile}&text={text}&reply_markup={buttons}'

            payload = {}
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload)
        profile = False
        try:
            second_profile = Profile.objects.get(id=meet.second_profile_id).contacts
            profile = True
        except Profile.DoesNotExist:
            profile = False
        if profile:
            print(f'**********meet.first_profile_id из every_saturday:{meet.first_profile_id}')
            text = f'✨ Хэй, как прошла встреча с @{get_username(main_bot_token, meet.first_profile_id)}? Можешь оценить встречу?'
            url = f'https://api.telegram.org/bot{main_bot_token}/sendMessage?chat_id={second_profile}&text={text}&reply_markup={buttons}'
            response = requests.request("POST", url, headers=headers, data=payload)
        meet.status = "non_active"
        meet.save()
