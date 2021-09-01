from django.urls import path

from ten_minutes_meet.views import Ready_to_Meet

urlpatterns = [

    path('ready_to_meet/', Ready_to_Meet.as_view())

]



