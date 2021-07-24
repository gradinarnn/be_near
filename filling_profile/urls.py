from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('press_ok', views.press_ok, name='press_ok'),
    path('login', views.login, name='login'),


]



