from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView, permission_classes
from rest_framework.permissions import IsAuthenticated
from app.models.homework import Homework, HomeworkUpload
from app.models.lessons import Lesson
from rest_framework.response import Response
from app.models.student import Student
from app.serializers.homework_serializer import HomeworkSerializer, HomeworkUploadSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from log.log import setup_logger

logger = setup_logger()


@permission_classes([IsAuthenticated])
class HomeworkUploadView(APIView):
    """
    API endpoint for students to upload homework.
    
    Allows students to submit their homework assignments.
    """

    @swagger_auto_schema(
        operation_summary="Upload Homework",
        operation_description="Submit homework for a lesson. Student uploads their completed work.",
        request_body=HomeworkUploadSerializer,
        responses={
            201: 'Homework saved successfully',
            404: 'Student not found',
            400: 'Validation error'
        }
    )
    def post(self, request):
        """Upload homework submission."""
        try:
            # Get student from user reference
            student = Student.objects.get(user=request.data['student'])
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if homework already submitted for this lesson
        lesson_id = request.data.get('lesson')
        if lesson_id:
            existing = HomeworkUpload.objects.filter(
                student=student,
                lesson_id=lesson_id
            ).first()
            
            if existing:
                return Response(
                    {"error": "Homework already submitted for this lesson"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Update data with student ID
        data = request.data.copy()
        data['student'] = student.id
        
        # Save homework submission
        serializer = HomeworkUploadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Homework saved"}, status=201)
        return Response({"error": serializer.errors}, status=400)



@permission_classes([IsAuthenticated])
class HomeworkPutMarkView(APIView):
    """
    API endpoint for teachers to grade homework.
    
    Allows teachers to mark homework as checked and assign grades.
    """

    @swagger_auto_schema(
        operation_summary="Grade Homework",
        operation_description="Mark homework as checked and assign a grade. Teacher access required.",
        request_body=HomeworkUploadSerializer,
        responses={
            200: 'Homework graded successfully',
            404: 'Homework not found',
            400: 'Validation error'
        }
    )
    def post(self, request, pk):
        """Grade and mark homework as checked."""
        if not pk:
            return Response({"error": "Homework ID is required"}, status=400)
        
        try:
            # Get homework submission
            homework = HomeworkUpload.objects.get(pk=pk)
        except HomeworkUpload.DoesNotExist:
            return Response({"error": "Homework not found"}, status=404)
        
        logger.info(f"Grading homework {pk}, current status: {homework.is_checked}")
        # Mark homework as checked
        homework.is_checked = True
        
        # Update homework with grade/feedback
        serializer = HomeworkUploadSerializer(homework, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Homework updated"}, status=200)
        return Response({"error": serializer.errors}, status=400)


@permission_classes([IsAuthenticated])
class HomeworkView(APIView):
    """
    API endpoint for managing homework assignments.
    
    Allows teachers to create homework assignments and view all submissions.
    """

    @swagger_auto_schema(
        operation_summary="Create Homework Assignment",
        operation_description="Create a new homework assignment for a lesson. Teacher access required.",
        request_body=HomeworkSerializer,
        responses={
            201: 'Homework assignment created',
            400: 'Validation error'
        }
    )
    def post(self, request):
        """Create a new homework assignment."""
        serializer = HomeworkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Homework created"}, status=201)
        return Response({"error": serializer.errors}, status=400)

    @swagger_auto_schema(
        operation_summary="List All Homework Submissions",
        operation_description="Retrieve all homework submissions from students.",
        responses={
            200: openapi.Response('List of homework submissions', HomeworkUploadSerializer(many=True))
        }
    )
    def get(self, request):
        """Retrieve all homework submissions."""
        homeworks = HomeworkUpload.objects.all()
        serializer = HomeworkUploadSerializer(homeworks, many=True)
        return Response(serializer.data, status=200)


class HomeworkDetailView(APIView):
    """
    API endpoint for managing specific homework assignments.
    
    Allows creating and updating homework assignments by ID.
    """

    @swagger_auto_schema(
        operation_summary="Create Homework (Alternative)",
        operation_description="Create a new homework assignment. Consider using HomeworkView POST instead.",
        request_body=HomeworkSerializer,
        responses={
            201: 'Homework created',
            400: 'Validation error'
        }
    )
    def post(self, request, pk):
        """Create a new homework assignment."""
        serializer = HomeworkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Homework created"}, status=201)
        return Response({"error": serializer.errors}, status=400)

    @swagger_auto_schema(
        operation_summary="Update Homework Assignment",
        operation_description="Update an existing homework assignment. Teacher access required.",
        request_body=HomeworkSerializer,
        responses={
            200: 'Homework updated',
            404: 'Homework not found',
            400: 'Validation error'
        }
    )
    def put(self, request, pk):
        """Update a homework assignment."""
        print(request.data)
        if not pk:
            return Response({"error": "Homework ID is required"}, status=400)
        
        try:
            # Get homework assignment
            homework = Homework.objects.get(pk=pk)
        except Homework.DoesNotExist:
            return Response({"error": "Homework not found"}, status=404)
        
        # Update homework
        serializer = HomeworkSerializer(homework, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Homework updated"}, status=200)
        return Response({"error": serializer.errors}, status=400)


@permission_classes([IsAuthenticated])
class LessonHomeworkView(APIView):
    """
    API endpoint for retrieving homework submissions for a specific lesson.
    
    Useful for teachers to view all student submissions for a particular lesson.
    """

    @swagger_auto_schema(
        operation_summary="Get Homework Submissions for a Lesson",
        operation_description="Retrieve all homework submissions for a specific lesson. Teachers can see all submissions.",
        responses={
            200: openapi.Response('List of homework submissions for the lesson', HomeworkUploadSerializer(many=True)),
            404: 'Lesson not found',
            400: 'Error retrieving homework'
        }
    )
    def get(self, request, lesson_id):
        """Retrieve homework submissions for a specific lesson."""
        # Verify lesson exists (raises Http404 if not found)
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        
        try:
            # Get all homework uploads for this lesson
            homework_uploads = HomeworkUpload.objects.filter(lesson=lesson).select_related('student', 'homework')
            
            serializer = HomeworkUploadSerializer(homework_uploads, many=True)
            logger.info(f"Retrieved {homework_uploads.count()} homework submissions for lesson {lesson_id}")
            
            return Response(serializer.data, status=200)
            
        except Exception as e:
            logger.error(f"Error retrieving homework for lesson {lesson_id}: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred while retrieving homework"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )