# import debug_toolbar
from django.urls import include, path
from django.conf import settings

from . import views
from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView, stop_meet_change_partner, \
    leave_feedback, filling_db, GetFeedbackFromUser

urlpatterns = [
    path('', views.index, name='index'),
    path('info_changer', views.info_changer, name='info_changer'),
    path('update_skills', views.update_skills, name='update_skills'),
    path('login', views.login, name='login'),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('stop_meeting', views.stop_meeting, name='stop_meeting'),
    path('stop_meet_change_partner/', stop_meet_change_partner.as_view()),
    path('leave_feedback/', leave_feedback.as_view()),
    path('filling_db/',filling_db.as_view()),
    path('getfeedbackfromuser/', GetFeedbackFromUser.as_view()),
    # path('new_schedule/', new_schedule.as_view())

    # path('__debug__/', include(debug_toolbar.urls)),



]



