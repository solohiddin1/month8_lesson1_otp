from django.urls import path
from app.models.attendence import Attendence
from app.views.media import media
from app.views.admin import TeacherCrud, admin_panel, teacher_panel
from app.views.attendence import AttendanceDetailView, AttendenceGetView, AttendenceView
from app.views.homework import HomeworkDetailView, HomeworkPutMarkView, HomeworkUploadView, HomeworkView
from app.views.lesson import LessonDetailView, LessonView
from app.views.student import StudentView, StudentsView
from app.views.user import register_view
from app.views.auth import (forgot_password_view, logout_view ,change_password_page, forgot_password, 
    home, reset_page, reset_password, student_dashboard, userlogin, userlogin_view, loginexistinguser,
    loginexistinguser_view, verify_user_email_view,
    verify, login, verify_user_email, change_password)
from app.views.teacher import TeacherCreateView, TeacherProfileView
from app.views.user import (register, 
     delete_user)
from app.views.groups import AddStudentGroupView, GroupCreate, GroupDetailView, GroupListView, StudentGroupsView, StudentsIngroupView, TeacherGroups

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    # path('user/',UserCreateView.as_view()),
    # path('login/',login,name='login'),
    # path('verify/',verify,name='verify'),

    # media
    # path('media/default.jpg/',media),


    # homework
    path('api/homework_get/',HomeworkView.as_view(), name='api_homework'),
    path('api/homework/<int:pk>/',HomeworkDetailView.as_view(), name='api_homework_detail'),
    path('api/homework_put_mark/<int:pk>/',HomeworkPutMarkView.as_view(), name='api_homework_detail'),
    path('api/homework_upload/',HomeworkUploadView.as_view(), name='api_homework_detail'),

    # student
    path('api/student/',StudentView.as_view(), name='student'),
    path('student_groups/',StudentGroupsView.as_view(), name="student_groups"),
    path('students/',StudentsView.as_view(), name='students'),
    
    # lesson
    path('create_lesson/',LessonView.as_view(),name="lesson"),
    
    # teacher
    path('api/teacher_profile/',TeacherProfileView.as_view(),name='teacher_profie_view'),
    path('api/teachers/',TeacherCreateView.as_view(),name='create_teacher_view'),
    path('api/teachers/<int:pk>/',TeacherCreateView.as_view(),name='teacher_detail'),
    path('teacher_crud/',TeacherCrud, name='teacher_crud'),
    path('api/teacher/groups/',TeacherGroups.as_view(), name='teacher_groups'),

    # groups
    path('add_student_to_group/',AddStudentGroupView.as_view(),name='add_student_to_group'),
    path('cr_gr/',GroupCreate.as_view(), name="cr_gr"),
    path('create_groups/',GroupListView.as_view(), name="groups"),
    path('create_groups/<int:pk>/',GroupDetailView.as_view(),name="group-detail"),
    path('api/group/<int:pk>/students/',StudentsIngroupView.as_view(),name="students_in_group"),

    # homework
    # path('homework_detail/<int:pk>/',LessonDetailView.as_view(),name="lesson_detail"),
    
    # lesson detail
    path('lesson_detail/<int:pk>/',LessonDetailView.as_view(),name="lesson_detail"),

    # attendence
    path('attendense/',AttendenceView.as_view()),
    path('attendense/',AttendenceGetView.as_view()),
    path('attendense/<int:pk>/',AttendanceDetailView.as_view()),
    
    # login
    path('userlogin/',userlogin,name='userlogin'),
    path('userlogin/view/',userlogin_view,name='userlogin_view'),

    path('login_existing_user/',loginexistinguser,name='login_existing_user'),
    path('login_existing_user/view',loginexistinguser_view,name='login_existing_user_view'),


    # log out0
    path('api/logout/',logout_view,name='logout'),


    # password
    path('change_password_page/',change_password_page,name='change_password_page'),
    path('api/change_password/',change_password,name='change_password'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('forgot_password/view/',forgot_password_view,name='forgot_password_view'),
    
    path('reset-password/<uidb64>/<token>/',reset_password, name='reset_password'),
    path('api/reset-password/<uiid64>/<token>/',reset_page, name='reset_page'),


    # auth
    path('verify_user_otp/',verify_user_email,name='verify_user_otp'),
    path('verify_user_otp/view',verify_user_email_view,name='verify_user_otp_view'),

    path('register_user/',register,name='register_user'),
    path('delete_user/<int:pk>/',delete_user, name="delete"),
    
    # token
    path('api/token/',TokenObtainPairView.as_view()),
    path('api/token/refresh/',TokenRefreshView.as_view()),

    path('',home, name='home'),
    path('admin_dashboard/',admin_panel, name='admin_dashboard'),
    path('teacher_dashboard/',teacher_panel, name='teacher_dashboard'),
    path('student_dashboard/',student_dashboard,name='student_dashboard'),


    # path('register/', register, name='register'),
    path('register_view/', register_view, name='register_view'),
]