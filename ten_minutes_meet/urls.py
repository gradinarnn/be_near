from django.urls import path

from ten_minutes_meet.views import Ready_to_Meet, Chatting

urlpatterns = [

    path('ready_to_meet/', Ready_to_Meet.as_view()),
    path('chatting/', Chatting.as_view()),

]



