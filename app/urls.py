from os import name
from django.urls import path
from app.views import lesson
from app.views.attendence import AttendenceView
from app.views.lesson import LessonView
from app.views.user import UserCreateView, userlogin
from app.views.teacher import TeacherCreateView
from app.views.user import (verify, login,register, 
    verify_user_email, change_password, 
    loginexistinguser, delete_user)
from app.views.groups import GroupCreate, GroupDetailView, GroupListView


urlpatterns = [
    # path('user/',UserCreateView.as_view()),
    path('teacher/',TeacherCreateView.as_view()),
    # path('login/',login,name='login'),
    # path('verify/',verify,name='verify'),
    path('attendense/',AttendenceView.as_view()),
    path('register_user/',register,name='register'),
    path('userlogin/',userlogin,name='userlogin'),
    path('verify_user_otp/',verify_user_email,name='verify_user_otp'),
    path('change_password/',change_password,name='change_password'),
    path('login_existing_user/',loginexistinguser,name='login_existing_user'),
    path('delete_user/<int:pk>/',delete_user, name="delete"),
    path('cr_gr/',GroupCreate.as_view(), name="cr_gr"),
    path('create_groups/',GroupListView.as_view(), name="groups"),
    path('create_groups/<int:pk>/',GroupDetailView.as_view(),name="group-detail"),
    path('create_lesson',LessonView.as_view(),name="lesson"),
]