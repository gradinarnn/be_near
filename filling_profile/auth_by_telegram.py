from django.contrib.auth import get_user_model
from rest_framework import exceptions


class Auth_by_telegram(object):
    def authenticate(self, request, contacts=None):

        try:
            profile = get_user_model().objects.get(contacts=contacts) #получаем profile по user_id Telegram'a
        except get_user_model().DoesNotExist:
            profile = None

        return profile
