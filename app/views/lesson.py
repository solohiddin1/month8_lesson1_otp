from django.core.signals import request_started
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.models.groups import Group
from app.models.homework import Homework
from app.models.student import Student
from app.models.teacher import Teacher
from app.serializers import lesson
from app.serializers.homework_serializer import HomeworkSerializer
from app.serializers.lesson import LessonSerializer

from rest_framework.views import APIView
from app.models.lessons import Lesson
from drf_yasg.utils import status, swagger_auto_schema
from drf_yasg import openapi
from log.log import setup_logger

logger = setup_logger()


@permission_classes([IsAuthenticated])
class LessonView(APIView):
    """
    API endpoint for managing lessons.
    
    Allows creating new lessons and listing all lessons.
    """

    @swagger_auto_schema(
        operation_summary="Create Lesson",
        operation_description="Create a new lesson for a group. Teacher access required.",
        request_body=LessonSerializer,
        responses={
            201: 'Lesson created successfully',
            400: 'Validation error'
        }
    )
    def post(self, request):
        """Create a new lesson."""
        lessons = request.data
        
        try:
            # Get teacher from user ID
            teacher_id = Teacher.objects.get(user_id=request.data['teacher'])
        except Teacher.DoesNotExist:
            return Response(
                {"error": "Teacher not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Update data with teacher ID
        data = lessons.copy()
        data['teacher'] = teacher_id.id
        
        # Create lesson
        serializer = LessonSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Lesson created by teacher {teacher_id.id}")
            return Response(
                {"message": "Lesson is created"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        operation_summary="List All Lessons",
        operation_description="Retrieve a list of all lessons in the system.",
        responses={
            200: openapi.Response('List of all lessons', LessonSerializer(many=True)),
            400: 'Error retrieving lessons'
        }
    )
    def get(self, request):
        """Retrieve all lessons."""
        try:
            lessons = Lesson.objects.all()
            serializer = LessonSerializer(lessons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving lessons: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


@permission_classes([IsAuthenticated])
class LessonDetailView(APIView):
    """
    API endpoint for managing lesson details.
    
    Supports retrieving, updating, and deleting lessons.
    Students can view lessons and their homework. Teachers can update and delete lessons.
    """

    @swagger_auto_schema(
        operation_summary="Get Lesson Details",
        operation_description="Retrieve lesson details. Students see lesson with their homework.",
        responses={
            200: 'Lesson details with homework (for students)',
            404: 'Lesson not found or student not enrolled',
            400: 'Error retrieving lesson'
        }
    )
    def get(self, request, pk):
        """Retrieve lesson details."""
        try:
            # Check if user is a student
            try:
                student = Student.objects.get(user=request.user)
                # Student view: get lesson and their homework
                lesson = get_object_or_404(Lesson, pk=pk, group__students_set=student)
                homework = Homework.objects.filter(lesson=lesson, student=student)
                
                lesson_serializer = LessonSerializer(lesson)
                homework_serializer = HomeworkSerializer(homework, many=True)

                return Response({
                    "lesson": lesson_serializer.data,
                    "homework": homework_serializer.data
                })
            except Student.DoesNotExist:
                # Non-student view: get lesson only
                lesson = get_object_or_404(Lesson, pk=pk)
                lesson_serializer = LessonSerializer(lesson)
                return Response({"lesson": lesson_serializer.data})
                
        except Exception as e:
            print(e)
            logger.error(f"Error retrieving lesson {pk}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Update Lesson",
        operation_description="Update lesson information. Can include homework and file uploads. Teacher access required.",
        request_body=LessonSerializer,
        responses={
            200: 'Lesson updated successfully',
            404: 'Lesson not found',
            400: 'Validation error'
        }
    )
    def put(self, request, pk):
        """Update lesson information."""
        # Prepare data with files
        data = request.data.copy()
        data.update(request.FILES)
        
        # Get lesson
        lesson = get_object_or_404(Lesson, pk=pk)
        data['teacher'] = lesson.teacher_id
        
        print(data, 'data======')
        
        # Create homework if provided
        homeworkserializer = HomeworkSerializer(data=request.data)
        if homeworkserializer.is_valid():
            homework = homeworkserializer.save()
            data['homework'] = homework.id
        
        print('\n  new data , === ', data)

        # Clean data: convert lists to single values
        clean_data = {k: v[0] if isinstance(v, list) else v for k, v in data.items()}

        # Update lesson
        lesson_serializer = LessonSerializer(lesson, data=clean_data, partial=True)
        if lesson_serializer.is_valid():
            lesson_serializer.save()
            logger.info(f"Lesson {pk} updated successfully")
            return Response({"message": "Lesson updated"}, status=status.HTTP_200_OK)
        
        return Response(
            {"error": lesson_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        operation_summary="Delete Lesson",
        operation_description="Delete a lesson. Teacher/Admin access required.",
        responses={
            200: 'Lesson deleted successfully',
            404: 'Lesson not found',
            400: 'Error deleting lesson'
        }
    )
    def delete(self, request, pk):
        """Delete a lesson."""
        lesson = get_object_or_404(Lesson, pk=pk)
        
        if lesson:
            lesson.delete()
            logger.info(f"Lesson {pk} deleted successfully")
            return Response(
                {"message": "Lesson deleted successfully"},
                status=status.HTTP_200_OK
            )
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class GroupLessonsView(APIView):
    """
    API endpoint for retrieving lessons for a specific group.
    
    Students can view lessons only for groups they are enrolled in.
    """

    @swagger_auto_schema(
        operation_summary="Get Group Lessons",
        operation_description="Retrieve all lessons for a specific group. Students only see lessons for their groups.",
        responses={
            200: openapi.Response('List of lessons for the group', LessonSerializer(many=True)),
            403: 'Student not enrolled in this group',
            404: 'Group not found',
            400: 'Error retrieving lessons'
        }
    )
    def get(self, request, group_id):
        """Retrieve lessons for a specific group."""
        try:
            # Verify group exists
            group = get_object_or_404(Group, pk=group_id)
            
            # If user is a student, verify they're enrolled in this group
            try:
                student = Student.objects.get(user=request.user)
                if not group.students_set.filter(id=student.id).exists():
                    return Response(
                        {"error": "You are not enrolled in this group"},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Student.DoesNotExist:
                # Non-students (teachers/admin) can view any group's lessons
                pass
            
            # Get lessons for this group
            lessons = Lesson.objects.filter(group=group).order_by('-created_at')
            serializer = LessonSerializer(lessons, many=True)
            
            logger.info(f"Retrieved {lessons.count()} lessons for group {group_id}")
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error retrieving lessons for group {group_id}: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )