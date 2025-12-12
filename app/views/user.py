from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.status import HTTP_400_BAD_REQUEST
from app.serializers_f.user_serializer import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from app.models import User
from rest_framework import permissions
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from app.serializers_f.student_serizlizer import StudentSerializer
from app.models.student import Student
from log.log import setup_logger
logger = setup_logger()


@permission_classes([IsAdminUser])
def register_view(request):
    return render(request,'register.html')


class StudentRegistrationAPIView(generics.CreateAPIView):
    """
    API endpoint for student registration.
    
    Creates a new student account and sends welcome email with credentials.
    The student user is marked with is_student flag.
    """
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Register Student",
        operation_description="Register a new student. Sends welcome email with login credentials.",
        responses={
            201: openapi.Response('Student registered successfully'),
            400: 'Validation error'
        }
    )
    def post(self, request, *args, **kwargs):
        """Create a new student account."""
        print('user register')
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Save student and get associated user
            student = serializer.save()
            user = student.user
            
            # Send welcome email with credentials
            send_mail(
                "You are registered",
                f"You can login using your email and password. Your email is {user.email}, your password is 123456",
                settings.ALTERNATIVE_EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            
            student.save()
            logger.info(f"Student registered successfully: {user.email}")
            
            # Mark user as student
            user.is_student = True
            user.save()
            logger.info(f"User registered successfully: {user.email}")
            
            return Response(
                {"success": True, "message": "User registered successfully."}, 
                status=201
            )
        
        print(serializer.errors)
        return Response(
            {"Error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )



# class UserCreateView(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class DeleteUserAPIView(generics.DestroyAPIView):
    """
    API endpoint for deleting a user.
    
    Deletes both the student record and associated user account.
    Only accessible by admin users.
    """
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_summary="Delete User",
        operation_description="Delete a student and their associated user account. Admin only.",
        responses={
            200: openapi.Response('User deleted successfully'),
            400: 'Error deleting user',
            404: 'Student not found'
        }
    )
    def delete(self, request, *args, **kwargs):
        """Delete student and associated user."""
        try:
            pk = kwargs.get('pk')
            student = Student.objects.get(pk=pk)
            user = student.user
            
            # Delete student and user
            student.delete()
            user.delete()
            
            logger.info(f"User deleted successfully: {user.email}")
            return Response(
                {"success": True, "message": "User deleted successfully!"},
                status=200
            )

        except Student.DoesNotExist:
            logger.warning(f"Student not found with pk: {pk}")
            return Response(
                {"success": False, "error": "Student not found"}, 
                status=404
            )
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            return Response(
                {"success": False, "error": str(e)}, 
                status=400
            )