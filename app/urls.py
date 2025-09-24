from os import name
from django.urls import path
from app.views.user import UserCreateView, userlogin
from app.views.teacher import TeacherCreateView
from app.views.user import (verify, login,register, 
    verify_user_email, change_password, 
    loginexistinguser, delete_user)
from app.views.groups import *


urlpatterns = [
    # path('user/',UserCreateView.as_view()),
    path('teacher/',TeacherCreateView.as_view()),
    # path('login/',login,name='login'),
    # path('verify/',verify,name='verify'),
    path('register_user/',register,name='register'),
    path('userlogin/',userlogin,name='userlogin'),
    path('verify_user_otp/',verify_user_email,name='verify_user_otp'),
    path('change_password/',change_password,name='change_password'),
    path('login_existing_user/',loginexistinguser,name='login_existing_user'),
    path('delete_user/<int:pk>/',delete_user, name="delete"),
    path('create_groups/',CreateGroupView.as_view(), name="groups"),
]