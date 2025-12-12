from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from app.models.student import Student
from app.serializers_f.student_serizlizer import StudentSerializer, StudentGetSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



@permission_classes([IsAdminUser])  
class StudentAllView(APIView):
    """
    API endpoint to retrieve all students.
    
    Returns a list of all students in the system.
    Only accessible by admin users.
    """

    @swagger_auto_schema(
        operation_summary="Get All Students",
        operation_description="Retrieve a list of all students. Admin access required.",
        responses={
            200: openapi.Response('List of all students', StudentGetSerializer(many=True)),
            400: 'Error retrieving students'
        }
    )
    def get(self, request):
        """Retrieve all students."""
        try:
            # Get all students from database
            student = Student.objects.all()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Serialize student data
        serializer = StudentGetSerializer(student, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])  
class StudentView(APIView):
    """
    API endpoint to retrieve the authenticated student's profile.
    
    Returns the profile information of the currently logged-in student,
    including email and phone number from the associated user account.
    """

    @swagger_auto_schema(
        operation_summary="Get Student Profile",
        operation_description="Retrieve the profile of the currently authenticated student.",
        responses={
            200: openapi.Response('Student profile with user details', StudentSerializer),
            404: 'Student not found',
            400: 'Error retrieving student'
        }
    )
    def get(self, request):
        """Retrieve the authenticated student's profile."""
        try:
            # Get student associated with current user
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Serialize student data
        serializer = StudentSerializer(student)
        data = serializer.data.copy()
        
        # Add user email and phone number to response
        data['email'] = student.user.email
        data['phone_number'] = student.user.phone_number
        
        return Response(data, status=status.HTTP_200_OK)


@permission_classes([IsAdminUser])
class StudentsView(APIView):
    """
    API endpoint to retrieve all students (admin view).
    
    Returns a list of all students in the system.
    Only accessible by admin users.
    """

    @swagger_auto_schema(
        operation_summary="Get All Students (Admin)",
        operation_description="Retrieve a list of all students. Admin access required.",
        responses={
            200: openapi.Response('List of all students', StudentSerializer(many=True))
        }
    )
    def get(self, request):
        """Retrieve all students (admin endpoint)."""
        # Get all students from database
        students = Student.objects.all()
        
        # Serialize student data
        serializer = StudentSerializer(students, many=True)
        print(serializer.data)
        
        return Response(serializer.data)