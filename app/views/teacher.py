from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# from ..serializers import UserSerializer
from app.models import teacher
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.user import User
from app.serializers.student_serializer import StudentSerializer
from app.serializers.teacher_serializer import TeacherCreateSerializer, TeacherAddUserSerializer, TeacherSerializer
from drf_yasg.utils import swagger_auto_schema
from log.log import setup_logger


logger = setup_logger()

@permission_classes([IsAuthenticated])
class TeacherProfileView(APIView):
    """
    API endpoint to retrieve the authenticated teacher's profile.
    
    Returns the profile information of the currently logged-in teacher,
    including email and phone number from the associated user account.
    """

    @swagger_auto_schema(
        operation_summary="Get Teacher Profile",
        operation_description="Retrieve the profile of the currently authenticated teacher.",
        responses={
            200: 'Teacher profile with user details',
            404: 'Teacher not found',
            400: 'Error retrieving teacher'
        }
    )
    def get(self, request):
        """Retrieve the authenticated teacher's profile."""
        print(request.user.id)
        try:
            # Get teacher associated with current user
            teacher = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            return Response(
                {"error": "Teacher model does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Serialize teacher data
        serializer = TeacherSerializer(teacher)

        # Add user email and phone number to response
        data = serializer.data.copy()
        data['email'] = teacher.user.email
        data['phone_number'] = teacher.user.phone_number
        print(data)
        
        return Response(data, status=status.HTTP_200_OK)


@permission_classes([IsAdminUser])
class TeacherCreateView(APIView):
    """
    API endpoint for managing teachers (CRUD operations).
    
    Supports creating, listing, updating, and deleting teachers.
    Only accessible by admin users.
    """

    @swagger_auto_schema(
        operation_summary="Create Teacher",
        operation_description="Create a new teacher account. Sends welcome email with credentials. Admin only.",
        request_body=TeacherCreateSerializer,
        responses={
            201: 'Teacher created successfully',
            400: 'Validation error'
        }
    )
    def post(self, request):
        """Create a new teacher."""
        try:
            serializer = TeacherCreateSerializer(data=request.data)
            if serializer.is_valid():
                # Save teacher and get associated user
                teacher = serializer.save()
                user = teacher.user
                
                # Send welcome email with credentials
                send_mail(
                    subject='Welcome to the Teacher Portal',
                    message=f'Hello {teacher.name},\n\nYour teacher account has been created successfully.\nYour email is {user.email} and your password is [123456]\n\nThank you for joining us!',
                    from_email='sirojiddinovsolohiddin961@gmail.com',
                    recipient_list=[user.email],
                    fail_silently=False
                )
                
                logger.info(f"Teacher created successfully: {user.email}")
                return Response(
                    TeacherSerializer(teacher).data,
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating teacher: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="List All Teachers",
        operation_description="Retrieve a list of all teachers with their groups. Admin only.",
        responses={
            200: 'List of all teachers',
            404: 'No teachers found'
        }
    )
    def get(self, request):
        """Retrieve all teachers."""
        try:
            # Optimize query with select_related and prefetch_related
            teachers = Teacher.objects.select_related('user').prefetch_related('teaching_groups').all()
            print(teachers)
            
            if teachers.exists():
                serializer = TeacherSerializer(teachers, many=True)
                return Response(serializer.data, status=200)
            return Response({"error": "No teachers found"}, status=404)
        except Exception as e:
            logger.error(f"Error retrieving teachers: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Update Teacher",
        operation_description="Update an existing teacher's information. Admin only.",
        request_body=TeacherCreateSerializer,
        responses={
            200: 'Teacher updated successfully',
            404: 'Teacher not found',
            400: 'Validation error'
        }
    )
    def put(self, request, pk=None):
        """Update teacher information."""
        try:
            teacher = Teacher.objects.get(pk=pk)
            serializer = TeacherCreateSerializer(teacher, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Teacher updated: {teacher.user.email}")
                return Response(TeacherSerializer(teacher).data, status=200)
            return Response(serializer.errors, status=400)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=404)
        except Exception as e:
            logger.error(f"Error updating teacher: {str(e)}")
            return Response({"error": str(e)}, status=400)

    @swagger_auto_schema(
        operation_summary="Delete Teacher",
        operation_description="Delete a teacher account. Admin only.",
        responses={
            200: 'Teacher deleted successfully',
            404: 'Teacher not found',
            400: 'Error deleting teacher'
        }
    )
    def delete(self, request, pk=None):
        """Delete a teacher."""
        try:
            teacher = Teacher.objects.get(pk=pk)
            email = teacher.user.email
            teacher.delete()
            logger.info(f"Teacher deleted: {email}")
            return Response({"message": "Teacher deleted successfully"}, status=200)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=404)
        except Exception as e:
            logger.error(f"Error deleting teacher: {str(e)}")
            return Response({"error": str(e)}, status=400)