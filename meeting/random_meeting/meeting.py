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

from meeting.random_meeting.change_meeting_status import change_meeting_status
from telegram_services.send_message import get_telegram_id, get_username
from telegram_services.send_message import send_message

"""  Запустить процес формирования встреч  """

def meeting():
    all_profiles = Profile_for_Metting.objects.all()

    while len(all_profiles) > 0:
        print(f'-------------Весь список до взятия первого: {all_profiles}---------------------')
        print(f'-------------Длинна списка len(all_profiles): {len(all_profiles)}---------------------')
        all_profiles = list(all_profiles)
        print(f'-------------all_profiles list: {all_profiles}---------------------')
        first_profile = all_profiles.pop(0)
        print(f'-------------Первый пользователь <profile_id>:<full_name>: {first_profile.profile.id}:{first_profile.profile.full_name}---------------------')
        print(f'-------------Весь список после взятия первого: {all_profiles}---------------------')

        selection_list = all_profiles.copy()

        meeting_success = False
        while (len(selection_list) > 0) and (not meeting_success):
            second_profile_number = random.randint(0, len(selection_list) - 1)

            second_profile = selection_list.pop(second_profile_number)
            print(f'-------------len(selection_list): {len(selection_list)}-------------------')
            print(f'-------------Второй пользователь: {second_profile.profile_id}-------------------')
            print(f'-------------Весь список после взятия второго: {all_profiles}---------------------')
            print(f'-------------Cписок в котором искался второй: {selection_list}---------------------')

            # if ..... проверка встречались ли first_profile и second_profile до этого

            meeting_list = list(Meet.objects.all().filter(Q(first_profile_id=first_profile.profile_id) | Q(second_profile_id=first_profile.profile_id)))

            print(f'-------------Список в котором {first_profile} есть: {meeting_list}---------------------')

            meeting_indicator = False
            for meet in meeting_list:
                print(f'-------------meet:{meet}')
                print(f'-------------second_profile.profile_id == meet.first_profile_id:{int(second_profile.profile_id) == int(meet.first_profile_id)}, second_profile.profile_id == meet.second_profile_id:{int(second_profile.profile_id) == int(meet.second_profile_id)} ---------------------')
                if (int(second_profile.profile_id) == int(meet.first_profile_id)) or (int(second_profile.profile_id) == int(meet.second_profile_id)):
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
                             text=f'Мы нашли тебе себеседника, Вот его профиль: @{get_username(bot_token=main_bot_token, user_id=second_profile.profile_id)}. Ему интересно: {second_profile.profile.skills}.Приятной встречи 🌱')

                send_message(bot_token=main_bot_token, user_id=second_profile.profile_id,
                             text=f'Мы нашли тебе себеседника, Вот его профиль: @{get_username(bot_token=main_bot_token, user_id=first_profile.profile_id)}. Ему интересно: {first_profile.profile.skills}.Приятной встречи 🌱')

                # меняем статус встречи первого пользователя на "meeting"
                change_meeting_status(user_id=first_profile.profile_id, status="meetting")

                # меняем статус встречи второго пользователя на "meeting"
                change_meeting_status(user_id=second_profile.profile_id, status="meetting")

                meeting_success = True
            else:

                print(f'------------Такая пара уже была--------------')
                print(f'-------------А весь список при этом: {all_profiles}---------------------')

            print(f'-------------len(selection_list): {len(selection_list)}-------------------')
            print(f'-------------not meeting_success: {not meeting_success}-------------------')

        if meeting_success == True:
            print(f'-------------Удаляем пользователя: {all_profiles[second_profile_number]}---------------------')
            all_profiles.pop(second_profile_number)


"""  Проверка в среду, удалось ли связаться с собеседником  """

def check_meeting_3_day():
    text = f'Привет, уже успел пообщаться с'
    buttons = InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Да, всё гуд',
                    callback_data=checking_meeting.new(status="ok_good!"),

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

            send_message(main_bot_token,first_profile,)
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
            change_meeting_status(user_id=meet.first_profile_id, status="not ready")

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
            change_meeting_status(user_id=meet.second_profile_id, status="not ready")
        meet.status = "non_active"
        meet.save()
