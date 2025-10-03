from django.urls import path
from app.models.attendence import Attendence
from app.views.attendence import AttendanceDetailView, AttendenceGetView, AttendenceView
from app.views.lesson import LessonDetailView, LessonView
from app.views.user import UserCreateView, register_view
from app.views.auth import (logout_view ,change_password_page, forgot_password, 
    home, reset_page, reset_password, userlogin, userlogin_view, loginexistinguser,
    loginexistinguser_view, verify_user_email_view,
    verify, login, verify_user_email, change_password)
from app.views.teacher import TeacherCreateView
from app.views.user import (register, 
     delete_user)
from app.views.groups import GroupCreate, GroupDetailView, GroupListView

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

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

    # login
    path('userlogin/',userlogin,name='userlogin'),
    path('userlogin/view/',userlogin_view,name='userlogin_view'),

    path('login_existing_user/',loginexistinguser,name='login_existing_user'),
    path('login_existing_user/view',loginexistinguser_view,name='login_existing_user_view'),

    path('api/logout/',logout_view,name='logout'),


    # password
    path('change_password_page/',change_password_page,name='change_password_page'),
    path('api/change_password/',change_password,name='change_password'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    
    path('reset-password/<uidb64>/<token>/',reset_password, name='reset_password'),
    path('api/reset-password/<uiid64>/<token>/',reset_page, name='reset_page'),


    # auth
    path('verify_user_otp/',verify_user_email,name='verify_user_otp'),
    path('verify_user_otp/view',verify_user_email_view,name='verify_user_otp_view'),

    path('register_user/',register,name='register'),
    path('delete_user/<int:pk>/',delete_user, name="delete"),
    
    # token
    path('api/token/',TokenObtainPairView.as_view()),
    path('api/token/refresh/',TokenRefreshView.as_view()),

    path('',home, name='home'),

    path('register/', register, name='register'),
    path('register_view/', register_view, name='register_view'),
]