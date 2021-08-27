import be_near.constants
import json
from filling_profile.send_notification import send_MEET_notification
import random
from be_near.constants import host, bot_token

import threading
import schedule
import time
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from filling_profile.models import Profile
import requests
import time




import jwt
import requests
from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import Filling_Profile_form
from .models import Meet, Profile, Profile_for_Metting, Skills, Categories
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
)


def index(request):

    token = request.GET.get('token')
    if token != None:
        contacts = request.GET.get('contacts')


        payload = jwt.decode(token, 'q', algorithms="HS256")
        user = Profile.objects.get(pk=payload['id'])

        print(f'---------view index user.contacts:{user.contacts}-------------------')
        print(f'---------view index contacts:{contacts}-------------------')
        print(f'---------view index user:{user}-------------------')



        if user.contacts==contacts:
            data = {"full_name": user.full_name,
                    "email": user.email,
                    "goal": user.goal,
                    "language": user.language,
                    "contacts": user.contacts}

            form = Filling_Profile_form(data)
            skills_editing_profile = user.skills
            if skills_editing_profile != None:
                skills_editing_profile_list = skills_editing_profile.split(',')
            else:
                skills_editing_profile_list = ''
            form.full_name = user.full_name
            form.email = user.email
            print(f'-----------------{form.full_name}------{form.email}--------------------------')



    else:
        form = Filling_Profile_form
        skills_editing_profile_list = ''
        skills_editing_profile = ''
    skills = Skills.objects.all()
    categoriess = Categories.objects.all()

    return render(request, 'filling_profile/profile_form.html',
              {'form': form, 'skills': skills, 'categoriess': categoriess,
               'skills_editing_profile': skills_editing_profile,
               'skills_editing_profile_list': skills_editing_profile_list})




def press_ok(request):
    if request.method == "POST":
        form = Filling_Profile_form(request.POST)
        prof = form
        print(f'**********prof.is_valid():{prof.is_valid()}*****************************')
        print(f'**********prof.errors:{prof.errors}*****************************')
        prof.skills = request.POST.get('skills_list')
        print(f'**********prof.skills:{prof.skills}*****************************')
        
        try:
            editing_profile = Profile.objects.get(email=request.POST.get('email'))
            editing_profile.full_name =request.POST.get('full_name')           
            editing_profile.email = request.POST.get('email')
            editing_profile.skills = request.POST.get('skills_list')
            editing_profile.goal = request.POST.get('goal')
            editing_profile.language = request.POST.get('language')
            editing_profile.contacts = request.POST.get('contacts')
            editing_profile.save()
        except Profile.DoesNotExist:
       
            prof.is_valid()
            
            prof.save()
       
      

    else:
        form = Filling_Profile_form
    
    skills = Skills.objects.all()
    categoriess = Categories.objects.all()

    return render(request, 'filling_profile/profile_form.html',
              {'form': form, 'skills': skills, 'categoriess': categoriess,
               'skills_editing_profile': editing_profile.skills,
               'skills_editing_profile_list': editing_profile.skills.split(',')})


def login(request):
    return render(request, 'login.html')


# Запустить процес формирования встреч
def meeting(request):

    all_profiles = Profile_for_Metting.objects.all()
   
    while len(all_profiles) > 0:
        print(f'-------------Весь список до взятия первого: {all_profiles}---------------------')
        all_profiles = list(all_profiles)
        print(f'-------------all_profiles list: {all_profiles}---------------------')
        first_profile = all_profiles.pop(0)
        print(f'-------------Первый пользователь: {first_profile.profile_id}---------------------')
        print(f'-------------Весь список после взятия первого: {all_profiles}---------------------')

        selection_list=all_profiles.copy()

        meeting_success=False
        while (len(selection_list) > 0) and (not meeting_success):
            second_profile_number = random.randint(0, len(selection_list) - 1)
            second_profile = selection_list.pop(second_profile_number)
            print(f'-------------Второй пользователь: {second_profile.profile_id}-------------------')
            print(f'-------------Весь список после взятия второго: {all_profiles}---------------------')
            print(f'-------------Cписок в котором ищется второй: {selection_list}---------------------')

            # if ..... проверка встречались ли first_profile и second_profile до этого


            meeting_list =list(Meet.objects.all().filter(first_profile_id = first_profile.profile_id))+list(Meet.objects.all().filter(second_profile_id = first_profile.profile_id))
            
            print(f'-------------Список в котором {first_profile} есть: {meeting_list}---------------------')

            meeting_indicator = False
            for meet in meeting_list:

                if (second_profile.profile_id == meet.first_profile_id) or (second_profile.profile_id == meet.second_profile_id):
                    meeting_indicator = True
                    print(f'-------------meeting_indicator = {meeting_indicator}. А весь список при этом: {all_profiles}---------------------')

            print(f'-------------meeting_indicator: {meeting_indicator}---------------------')
            if meeting_indicator == False:
                print(f'------------Пара сформирована--------------')
                meeting  = Meet(first_profile_id=first_profile.profile_id, second_profile_id = second_profile.profile_id, status = 'active')
                print(f'----meeting:{meeting}--------------')
                meeting.save()

                
                send_MEET_notification(first_profile.profile_id,second_profile.profile_id,'Мы нашли тебе себеседника', 'Мы нашли тебе себеседника')

                # меняем статус встречи первого пользователя на "meeting"
                token_value = Profile.objects.get(id =first_profile.profile_id).token
                payload_data = {"meeting_status":"meetting"}
                payload_dict = {"profile":payload_data}
                payload = json.dumps(payload_dict)

                url = host +"/filling_profile/user/"
                token = 'Bearer '+token_value
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }
                response = requests.request("PATCH", url, headers=headers, data=payload)

                # меняем статус встречи второго пользователя на "meeting"
                token_value = Profile.objects.get(id =second_profile.profile_id).token
                payload_data = {"meeting_status":"meetting"}
                payload_dict = {"profile":payload_data}
                payload = json.dumps(payload_dict)

                url = host+"/filling_profile/user/"
                token = 'Bearer '+token_value
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }
                response = requests.request("PATCH", url, headers=headers, data=payload)

                

                meeting_success=True
            else:
                
                print(f'------------Такая пара уже была--------------')
                print(f'-------------А весь список при этом: {all_profiles}---------------------')

        if meeting_success == True:
            print(f'-------------Удаляем пользователя: {all_profiles[second_profile_number]}---------------------')
            all_profiles.pop(second_profile_number)



# Остановить все встречи и назначить статус участников "waitting"
def stop_meeting(request):
    active_meets = Meet.objects.all().filter(status = 'active')
    for meet in active_meets:
        meet.status = "non_active"
        meet.save()
        
        first_profile = Profile.objects.get(id=meet.first_profile_id)
        first_profile.meeting_status="waitting"
        first_profile.save()
        second_profile = Profile.objects.get(id=meet.second_profile_id)
        second_profile.meeting_status="waitting"
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
    all_meeting = Meet.objects.all().filter(status = 'active')






class stop_meet_change_partner(APIView):
    permission_classes = (AllowAny,)
    

    def post(self, request):
        profile_id = Profile.objects.get(contacts=request.data.get('profile_id', {})).id
        machine_token = request.data.get('machine_token', {})
        if machine_token == be_near.constants.a:


            q=Meet.objects.all().filter(status = 'active').filter(first_profile_id = profile_id)
            w=Meet.objects.all().filter(status = 'active').filter(second_profile_id = profile_id)
            for qq in q:
                qq.status = 'non_active'
                user_id_first = Profile.objects.get(id=qq.first_profile_id).contacts
                user_id_second = Profile.objects.get(id=qq.second_profile_id).contacts
                send_MEET_notification(user_id_first,user_id_second,'Встреча отменена, нам очень жаль 🤧', 'Встреча отменена, нам очень жаль 🤧')
                qq.save()
                token1 = Profile.objects.get(contacts = user_id_first).token
                payload_data = {"meeting_status":'waitting'}

                payload_dict = {"profile":payload_data}

                payload = json.dumps(payload_dict)


                url = host+"/filling_profile/user/"


                token = 'Bearer '+token1
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }
                response = requests.request("PATCH", url, headers=headers, data=payload)

                token2 = Profile.objects.get(contacts = user_id_second).token
                payload_data = {"meeting_status":'waitting'}

                payload_dict = {"profile":payload_data}

                payload = json.dumps(payload_dict)


                url = host+"/filling_profile/user/"


                token = 'Bearer '+token2
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }
                response = requests.request("PATCH", url, headers=headers, data=payload)

            
            for ww in w:
                ww.status = 'non_active'
                user_id_first = Profile.objects.get(id=ww.first_profile_id).contacts
                user_id_second = Profile.objects.get(id=ww.second_profile_id).contacts
                send_MEET_notification(user_id_first,user_id_second,'Встреча отменена, нам очень жаль 🤧', 'Встреча отменена, нам очень жаль 🤧')
                ww.save()
                token1 = Profile.objects.get(contacts = user_id_first).token
                payload_data = {"meeting_status":'waitting'}

                payload_dict = {"profile":payload_data}

                payload = json.dumps(payload_dict)


                url = host+"/filling_profile/user/"


                token = 'Bearer '+token1
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }
                response = requests.request("PATCH", url, headers=headers, data=payload)

                token2 = Profile.objects.get(contacts = user_id_second).token
                payload_data = {"meeting_status":'waitting'}

                payload_dict = {"profile":payload_data}

                payload = json.dumps(payload_dict)


                url = host+"/filling_profile/user/"


                token = 'Bearer '+token2
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }
                response = requests.request("PATCH", url, headers=headers, data=payload)

            return Response('ok', status=status.HTTP_200_OK)






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
    schedule.every().day.at("12:00").do(check_meeting_3_day)


    while True:  # этот цикл отсчитывает время. Он обязателен.
        schedule.run_pending()
        time.sleep(1)
    





job_thread = threading.Thread(target=run_threaded)
job_thread.start()