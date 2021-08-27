from be_near.constants import bot_token

import threading
import schedule
import time
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from .models import Meet, Profile




def check_meeting_3_day():
    checking_meeting= CallbackData("first_button", "status")
    text = f'🙌 Привет! Уже успел пообщаться с собеседником?'
    a = InlineKeyboardMarkup(
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
        print(f"*")
        if profile:
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={first_profile}&text={text}&reply_markup={a}'

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
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={second_profile}&text={text}&reply_markup={a}'
            response = requests.request("POST", url, headers=headers, data=payload)


def run_threaded():
    schedule.every().day.at("13:00").do(check_meeting_3_day,)


    while True:  # этот цикл отсчитывает время. Он обязателен.
        print(f"-")
        schedule.run_pending()
        time.sleep(1)
    





job_thread = threading.Thread(target=run_threaded)
job_thread.start()