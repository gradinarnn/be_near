from django.shortcuts import render
from django.db.models import Q

import be_near.constants
import json
from filling_profile.send_notification import send_MEET_notification
import random
from be_near.constants import host, bot_token
from filling_profile.telegram_function import username_from_id
from filling_profile.CallbackData import checking_meeting, meeting_feedback

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
from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ten_minutes_meet.models import Ten_Minutes_Profile_List


class Ready_to_Meet(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        # Получаем данные пользователя
        profile_id = Profile.objects.get(contacts=request.data.get('profile_id', {})).id
        machine_token = request.data.get('machine_token', {})

        # Сравниваем, наш ли это бот
        if machine_token == be_near.constants.a:
            try:
                profile = Ten_Minutes_Profile_List.objects.get(profile=Profile.objects.get(id=profile_id))
                profile_exist = True
                print(f'Профиль найден')
            except Ten_Minutes_Profile_List.DoesNotExist:
                profile_exist = False
                print(f'Профиль не найден')

            if not profile_exist:
                ten_minutes_profile = Ten_Minutes_Profile_List(profile=Profile.objects.get(id=profile_id))
                ten_minutes_profile.save()











            return Response('ok', status=status.HTTP_200_OK)
        else:
            return Response('not_ok', status=status.is_client_error(400))
