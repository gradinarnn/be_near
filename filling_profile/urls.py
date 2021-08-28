from django.urls import path


from . import views
from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView, stop_meet_change_partner

urlpatterns = [
    path('', views.index, name='index'),
    path('press_ok', views.press_ok, name='press_ok'),
    path('login', views.login, name='login'),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('meeting', views.meeting, name='meeting'),
    path('stop_meeting', views.stop_meeting, name='stop_meeting'),
    path('stop_meet_change_partner/', stop_meet_change_partner.as_view())


]



