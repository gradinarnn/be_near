from django.urls import path


from . import views
from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView

urlpatterns = [
    path('', views.index, name='index'),
    path('press_ok', views.press_ok, name='press_ok'),
    path('login', views.login, name='login'),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('meeting', views.meeting, name='meeting')


]



