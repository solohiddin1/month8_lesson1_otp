from django.urls import path
from app.views.user import UserCreateView
from app.views.teacher import TeacherCreateView

urlpatterns = [
    path('user/',UserCreateView.as_view()),
    path('teacher/',TeacherCreateView.as_view()),
]