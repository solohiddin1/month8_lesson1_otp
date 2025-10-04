from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# from ..serializers import UserSerializer
from app.models import teacher
from app.models.teacher import Teacher
from app.models.user import User
from app.serializers_f.teacher_serializer import TeacherCreateSerializer, TeacherAddUserSerializer, TeacherSerializer
from drf_yasg.utils import swagger_auto_schema



@permission_classes([IsAdminUser])
class TeacherCreateView(APIView):
    @swagger_auto_schema(request_body=TeacherCreateSerializer)
    def post(self,request):
        try:
            serializer = TeacherCreateSerializer(data=request.data)
            if serializer.is_valid():
                teacher = serializer.save()
                user = teacher.user
                send_mail(
                subject = 'Welcome to the Teacher Portal',
                message = f'Hello {teacher.name},\n\nYour teacher account has been created successfully.\n Your email is {user.email} and your password is [123456]\n\nThank you for joining us!',
                from_email = 'sirojiddinovsolohiddin961@gmail.com',
                recipient_list = [user.email],
                fail_silently = False
                )
                return Response(TeacherSerializer(teacher).data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)})
    
    def get(self,request):
        try:
            # teachers = Teacher.objects.all()
            teachers = Teacher.objects.select_related('user').all()
            print(teachers)
            for i in teachers:
                print(i)
                print(i.name,)
            if teachers.exists():
                serializer = TeacherSerializer(teachers,many=True)
                return Response(serializer.data,status=200)
            return Response({"error ": "No teachers fuond"},status=404)
        except Exception as e:
            return Response({"error":str(e)})


    def put(self):
        pass

    def delete(self):
        pass