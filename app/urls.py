from django.urls import path
from app.views.user import UserCreateView
from app.views.teacher import TeacherCreateView
from app.views.user import verify, login,register

urlpatterns = [
    path('user/',UserCreateView.as_view()),
    path('teacher/',TeacherCreateView.as_view()),
    path('login/',login,name='login'),
    path('verify/',verify,name='verify'),
    path('register/',register)
]