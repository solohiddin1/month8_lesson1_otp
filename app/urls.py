from django.urls import path
from app.models.attendence import Attendence
from app.views.attendence import AttendanceDetailView, AttendenceGetView, AttendenceView
from app.views.lesson import LessonDetailView, LessonView
from app.views.user import UserCreateView
from app.views.auth import forgot_password, home, reset_page, reset_password, userlogin, verify, login, verify_user_email, change_password
from app.views.teacher import TeacherCreateView
from app.views.user import (register, 
     delete_user)
from app.views.groups import GroupCreate, GroupDetailView, GroupListView


urlpatterns = [
    # path('user/',UserCreateView.as_view()),
    # path('login/',login,name='login'),
    # path('verify/',verify,name='verify'),
    
    #models
    # path('teacher/',TeacherCreateView.as_view()),
    # path('attendense/',AttendenceView.as_view()),
    # path('attendense/<int:pk>/',AttendanceDetailView.as_view()),
    # path('cr_gr/',GroupCreate.as_view(), name="cr_gr"),
    # path('create_groups/',GroupListView.as_view(), name="groups"),
    # path('create_groups/<int:pk>/',GroupDetailView.as_view(),name="group-detail"),
    # path('create_lesson',LessonView.as_view(),name="lesson"),
    # path('lesson_detail',LessonDetailView.as_view(),name="lesson"),
    path('attendense/',AttendenceGetView.as_view()),

    # auth
    path('register_user/',register,name='register'),
    path('userlogin/',userlogin,name='userlogin'),
    path('verify_user_otp/',verify_user_email,name='verify_user_otp'),
    path('change_password/',change_password,name='change_password'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    # path('delete_user/<int:pk>/',delete_user, name="delete"),
    # path('login_existing_user/',loginexistinguser,name='login_existing_user'),
    # path('api/token/',ObtainTokenView.as_view()),
    # path('api/token/refresh/',RefreshTokenView.as_view()),

    path('reset-password/<uidb64>/<token>/',reset_password, name='reset_password'),
    path('api/reset-password/<uiid64>/<token>/',reset_page, name='reset_page'),
    path('home/',home, name='home'),
]