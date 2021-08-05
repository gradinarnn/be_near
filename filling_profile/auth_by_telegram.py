
from django.contrib.auth import get_user_model



class Auth_by_telegram(object):
    def authenticate(self, request, contacts=None):

        user = get_user_model().objects.get(contacts=contacts)

        if user is None:
            return None
        else:
            return user
