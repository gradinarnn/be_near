
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




# Запустить процес формирования встреч
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
                             text=f'Мы нашли тебе себеседника @{get_username(bot_token=main_bot_token, user_id=second_profile.profile_id)}')

                send_message(bot_token=main_bot_token, user_id=second_profile.profile_id,
                             text=f'Мы нашли тебе себеседника @{get_username(bot_token=main_bot_token, user_id=first_profile.profile_id)}')

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