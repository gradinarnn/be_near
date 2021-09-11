from sched import scheduler

from django.db.models import Q

import be_near.constants
import json
import random

from be_near import constants
from be_near.constants import host, main_bot_token
from filling_profile.CallbackData import checking_meeting, meeting_feedback

from meeting.random_meeting.change_meeting_status import change_meeting_status

import threading
import schedule
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from filling_profile.models import Profile
import requests
import time

import jwt
import requests
from django.shortcuts import render,redirect
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from meeting.random_meeting.meeting import meeting, check_meeting_3_day, every_saturday
from telegram_services.send_message import get_telegram_id, get_username
from telegram_services.send_message import send_message
from .filling_db import doing_filling_db
from .forms import Filling_Profile_form
from .models import Meet, Profile, Profile_for_Metting, Skill, Category
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
)

def token_decoder(req):
    token = req.GET.get('token')
    if token != None:
        contacts = req.GET.get('contacts')

        playload = jwt.decode(token, 'q', algorithms="HS256")
        user = Profile.objects.get(pk=playload['id'])

        return user
    else:
        return None

def index(request):
    # На этом этапе склеиваем выбранные навыки и те, что есть в целом
    # user.contacts = telegeam and others socials network

    """ Обычный вывод информации по юзеру на странице с профилем """

    token = request.GET.get('token')
    if token != None:
        contacts = request.GET.get('contacts')

        payload = jwt.decode(token, 'q', algorithms="HS256")  # Передача id-шника
        user = Profile.objects.get(pk=payload['id'])
        # print(request.user)

        if user.contacts == contacts:
            data = {"full_name": user.full_name,
                    "email": user.email,
                    "goal": user.goal,
                    "language": user.language,
                    "contacts": user.contacts}

            forms = Filling_Profile_form(data)

            # skills = user.skills  # Получаю текущий список скиллов юзера
            # Убираю проверку, будет доступна на выводе
            # if skills_editing_profile != None:
            #     skills_editing_profile_list = skills_editing_profile.split(',')
            # else:
            #     skills_editing_profile_list = ''

            forms.full_name = user.full_name
            forms.email = user.email
            # print(f'-----------------{form.full_name}------{form.email}--------------------------')



    else:
        forms = Filling_Profile_form
        user = ''

    skills = Skill.objects.all()
    categories = Category.objects.all()

    return render(request, 'filling_profile/profile_form.html',
                  {'user': user, 'skills': skills, 'categories': categories, 'forms': forms})


def press_ok(request):
    if request.method == "POST":
        forms = Filling_Profile_form(request.POST)
        prof = forms
        print(f'**********prof.is_valid():{prof.is_valid()}*****************************')
        print(f'**********prof.errors:{prof.errors}*****************************')
        prof.skills = request.POST.get('skills_list')
        print(f'**********prof.skills:{prof.skills}*****************************')

        try:
            # Принимаем обновлённые данные
            # editing_profile = Profile.objects.get(email=request.POST.get('email'))
            editing_profile = request.user
            editing_profile.full_name = request.POST.get('full_name')
            editing_profile.email = request.POST.get('email')
            editing_profile.skills = request.POST.get('skills_list')
            editing_profile.goal = request.POST.get('goal')
            editing_profile.language = request.POST.get('language')
            editing_profile.contacts = request.POST.get('contacts')
            editing_profile.save()

        except Profile.DoesNotExist:
            prof.is_valid()

            prof.save()

        user = editing_profile



    else:
        forms = Filling_Profile_form
        user = request.user

    skills = Skill.objects.all()
    categories = Category.objects.all()

    return render(request, 'filling_profile/profile_form.html',
                  {'user': user, 'forms': forms, 'skills': skills, 'categories': categories})


def update_skills(request):
    if request.method == "POST":
        forms = Filling_Profile_form(request.POST)
        try:
            editing_profile = request.user
            editing_profile.skills = request.POST.get('skills-texts')
            editing_profile.save()

        except Profile.DoesNotExist:
            print('Do something')

        user = editing_profile

    else:
        user = request.user
        forms = Filling_Profile_form


    skills = Skill.objects.all()
    categories = Category.objects.all()

    # return redirect(request.headers['REFERER'],
    #                 {'user': user, 'forms': forms, 'skills': skills, 'categories': categories})

    return render(request, 'filling_profile/profile_form.html',
                  {'user': user, 'forms': forms, 'skills': skills, 'categories': categories})


def login(request):
    return render(request, 'login.html')


# # Запустить процес формирования встреч
# def meeting():
#     all_profiles = Profile_for_Metting.objects.all()
#
#     while len(all_profiles) > 0:
#         print(f'-------------Весь список до взятия первого: {all_profiles}---------------------')
#         all_profiles = list(all_profiles)
#         print(f'-------------all_profiles list: {all_profiles}---------------------')
#         first_profile = all_profiles.pop(0)
#         print(f'-------------Первый пользователь: {first_profile.profile_id}---------------------')
#         print(f'-------------Весь список после взятия первого: {all_profiles}---------------------')
#
#         selection_list = all_profiles.copy()
#
#         meeting_success = False
#         while (len(selection_list) > 0) and (not meeting_success):
#             second_profile_number = random.randint(0, len(selection_list) - 1)
#             second_profile = selection_list.pop(second_profile_number)
#             print(f'-------------Второй пользователь: {second_profile.profile_id}-------------------')
#             print(f'-------------Весь список после взятия второго: {all_profiles}---------------------')
#             print(f'-------------Cписок в котором ищется второй: {selection_list}---------------------')
#
#             # if ..... проверка встречались ли first_profile и second_profile до этого
#
#             meeting_list = list(Meet.objects.all().filter(first_profile_id=first_profile.profile_id)) + list(
#                 Meet.objects.all().filter(second_profile_id=first_profile.profile_id))
#
#             print(f'-------------Список в котором {first_profile} есть: {meeting_list}---------------------')
#
#             meeting_indicator = False
#             for meet in meeting_list:
#
#                 if (second_profile.profile_id == meet.first_profile_id) or (
#                         second_profile.profile_id == meet.second_profile_id):
#                     meeting_indicator = True
#                     print(
#                         f'-------------meeting_indicator = {meeting_indicator}. А весь список при этом: {all_profiles}---------------------')
#
#             print(f'-------------meeting_indicator: {meeting_indicator}---------------------')
#             if not meeting_indicator:
#                 print(f'------------Пара сформирована--------------')
#                 meeting = Meet(first_profile_id=first_profile.profile_id, second_profile_id=second_profile.profile_id,
#                                status='active')
#                 print(f'----meeting:{meeting}--------------')
#                 meeting.save()
#
#                 send_message(bot_token=main_bot_token, user_id=first_profile.profile_id,
#                              text=f'Мы нашли тебе себеседника @{get_username(bot_token=main_bot_token, user_id=second_profile.profile_id)}')
#
#                 send_message(bot_token=main_bot_token, user_id=second_profile.profile_id,
#                              text=f'Мы нашли тебе себеседника @{get_username(bot_token=main_bot_token, user_id=first_profile.profile_id)}')
#
#                 # меняем статус встречи первого пользователя на "meeting"
#                 token_value = Profile.objects.get(id=first_profile.profile_id).token
#                 payload_data = {"meeting_status": "meetting"}
#                 payload_dict = {"profile": payload_data}
#                 payload = json.dumps(payload_dict)
#
#                 url = host + "/filling_profile/user/"
#                 token = 'Bearer ' + token_value
#                 headers = {
#                     'Authorization': token,
#                     'Content-Type': 'application/json'
#                 }
#                 response = requests.request("PATCH", url, headers=headers, data=payload)
#
#                 # меняем статус встречи второго пользователя на "meeting"
#                 token_value = Profile.objects.get(id=second_profile.profile_id).token
#                 payload_data = {"meeting_status": "meetting"}
#                 payload_dict = {"profile": payload_data}
#                 payload = json.dumps(payload_dict)
#
#                 url = host + "/filling_profile/user/"
#                 token = 'Bearer ' + token_value
#                 headers = {
#                     'Authorization': token,
#                     'Content-Type': 'application/json'
#                 }
#                 response = requests.request("PATCH", url, headers=headers, data=payload)
#
#                 meeting_success = True
#             else:
#
#                 print(f'------------Такая пара уже была--------------')
#                 print(f'-------------А весь список при этом: {all_profiles}---------------------')
#
#         if meeting_success == True:
#             print(f'-------------Удаляем пользователя: {all_profiles[second_profile_number]}---------------------')
#             all_profiles.pop(second_profile_number)


# Остановить все встречи и назначить статус участников "waitting"
def stop_meeting(request):
    active_meets = Meet.objects.all().filter(status='active')
    for meet in active_meets:
        meet.status = "non_active"
        meet.save()

        first_profile = Profile.objects.get(id=meet.first_profile_id)
        first_profile.meeting_status = "waitting"
        first_profile.save()
        second_profile = Profile.objects.get(id=meet.second_profile_id)
        second_profile.meeting_status = "waitting"
        second_profile.save()


class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        profile = request.data.get('profile', {})

        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.serializer_class(data=profile)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('profile', {})
        user["companion"] = "asdadfsgsdfg"

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        print(f'**********{serializer.data}')

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    # работает по запросу GET
    def retrieve(self, request, *args, **kwargs):
        # Здесь нечего валидировать или сохранять. Мы просто хотим, чтобы
        # сериализатор обрабатывал преобразования объекта User во что-то, что
        # можно привести к json и вернуть клиенту.
        user = request.data.get('profile', {})
        serializer = self.serializer_class(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # работает по запросу PATCH
    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('profile', {})
        # Паттерн сериализации, валидирования и сохранения - то, о чем говорили
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


def check_meeting(request):
    # получаем все встречи
    all_meeting = Meet.objects.all().filter(status='active')


class stop_meet_change_partner(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        profile_id = Profile.objects.get(contacts=request.data.get('profile_id', {})).id
        machine_token = request.data.get('machine_token', {})
        if machine_token == be_near.constants.a:

            q = Meet.objects.all().filter(status='active').filter(first_profile_id=profile_id)
            w = Meet.objects.all().filter(status='active').filter(second_profile_id=profile_id)
            for qq in q:
                qq.status = 'non_active'
                user_id_first = Profile.objects.get(id=qq.first_profile_id).contacts
                user_id_second = Profile.objects.get(id=qq.second_profile_id).contacts

                send_message(bot_token=main_bot_token, telegram_id=get_telegram_id(user_id_first),
                             text=f'Встреча отменена, нам очень жаль 🤧')
                send_message(bot_token=main_bot_token, telegram_id=get_telegram_id(user_id_second),
                             text=f'Встреча отменена, нам очень жаль 🤧')

                qq.save()
                token1 = Profile.objects.get(contacts=user_id_first).token
                payload_data = {"meeting_status": 'waitting'}

                payload_dict = {"profile": payload_data}

                payload = json.dumps(payload_dict)

                url = host + "/filling_profile/user/"

                token = 'Bearer ' + token1
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }
                response = requests.request("PATCH", url, headers=headers, data=payload)

                token2 = Profile.objects.get(contacts=user_id_second).token
                payload_data = {"meeting_status": 'waitting'}

                payload_dict = {"profile": payload_data}

                payload = json.dumps(payload_dict)

                url = host + "/filling_profile/user/"

                token = 'Bearer ' + token2
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }
                response = requests.request("PATCH", url, headers=headers, data=payload)

            for ww in w:
                ww.status = 'non_active'
                user_id_first = Profile.objects.get(id=ww.first_profile_id).contacts
                user_id_second = Profile.objects.get(id=ww.second_profile_id).contacts

                send_message(bot_token=main_bot_token, telegram_id=get_telegram_id(user_id_first),
                             text=f'Встреча отменена, нам очень жаль 🤧')
                send_message(bot_token=main_bot_token, telegram_id=get_telegram_id(user_id_second),
                             text=f'Встреча отменена, нам очень жаль 🤧')

                ww.save()
                token1 = Profile.objects.get(contacts=user_id_first).token
                payload_data = {"meeting_status": 'waitting'}

                payload_dict = {"profile": payload_data}

                payload = json.dumps(payload_dict)

                url = host + "/filling_profile/user/"

                token = 'Bearer ' + token1
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }
                response = requests.request("PATCH", url, headers=headers, data=payload)

                token2 = Profile.objects.get(contacts=user_id_second).token
                payload_data = {"meeting_status": 'waitting'}

                payload_dict = {"profile": payload_data}

                payload = json.dumps(payload_dict)

                url = host + "/filling_profile/user/"

                token = 'Bearer ' + token2
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }
                response = requests.request("PATCH", url, headers=headers, data=payload)

            return Response('ok', status=status.HTTP_200_OK)






#
# def writte():
#     print(f'*************ЖИ ЕСТЬ******************')
#
#
# def run_threaded():
#
#
#
#     while True:  # этот цикл отсчитывает время. Он обязателен.
#         schedule.run_pending()
#         time.sleep(1)
#
#
# job_thread = threading.Thread(target=run_threaded)
# job_thread.start()
#
#
# class new_schedule(APIView):
#
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         time1= request.data.get('time')
#         print(f'*********time:{time1}')
#         schedule.every().day.at(str(time1)).do(writte, )
#         print(f"***********предстоящая очередь без всего:{scheduler.queue}")
#         print(f"***********предстоящая очередь.time:{scheduler.queue.time}")
#         print(f"***********предстоящая очередь.priority:{scheduler.queue.priority}")
#         print(f"***********предстоящая очередь.action:{scheduler.queue.action}")
#         return Response('ok', status=status.HTTP_200_OK)


def run_threaded():
    schedule.every().monday.at("08:00").do(meeting, )
    schedule.every().wednesday.at("08:00").do(check_meeting_3_day, )
    schedule.every().saturday.at("16:00").do(every_saturday, )

    while True:  # этот цикл отсчитывает время. Он обязателен.
        schedule.run_pending()
        time.sleep(1)


job_thread = threading.Thread(target=run_threaded)
job_thread.start()


class leave_feedback(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        # Получаем данные пользователя
        profile_id = Profile.objects.get(contacts=request.data.get('profile_id', {})).id
        machine_token = request.data.get('machine_token', {})
        feedback = request.data.get('feedback', {})

        # Сравниваем, наш ли это бот
        if machine_token == be_near.constants.a:
            # Определяем какой пользователь(первый или второй) прислал feedback
            meet = Meet.objects.all().filter(Q(first_profile_id=profile_id) | Q(second_profile_id=profile_id),
                                             status='non_active').latest('date_meeting')
            if profile_id == int(meet.first_profile_id):
                meet.first_feedback = feedback
            elif profile_id == int(meet.second_profile_id):
                meet.second_feedback = feedback

            meet.save()

            return Response('ok', status=status.HTTP_200_OK)
        else:
            return Response('not_ok', status=status.is_client_error(400))


# для заполнения БД скиллами и категориями передать в параметрах запроса "machine_token":"значение"
class filling_db(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        machine_token = request.data.get('machine_token', {})
        if machine_token == constants.a:
            doing_filling_db()

        return Response('ok', status=status.HTTP_200_OK)


class GetFeedbackFromUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user_telegram = request.data.get('user_telegram', {})
        profile = Profile.objects.get(contacts=user_telegram)
        meet = list(Meet.objects.all().filter(Q(first_profile_id=profile.id) | Q(second_profile_id=profile.id),
                                               status='active'))
        if len(meet) == 1:

            change_meeting_status(meet[0].first_profile_id, "not ready")
            change_meeting_status(meet[0].second_profile_id, "not ready")
            meet[0].status = "non_active"
            meet[0].save()

            if (meet[0].first_feedback is not None) or (meet[0].second_feedback is not None):

                return Response('true', status=status.HTTP_200_OK)
            else:
                return Response('false', status=status.HTTP_200_OK)

        else:
            print(f'*********Количество записей в списке встреч={len(meet)}')

        return Response('many meets', status=status.HTTP_200_OK)

