from pickletools import pystring
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from app.models.attendance import Attendance
from app.models.groups import Group
from app.models.teacher import Teacher
from app.pagination import CustomPagination
from app.serializers import AttendanceSerializer
from rest_framework.response import Response
from rest_framework import status
from app.permissions import TeacherPermissions
from log.log import setup_logger

logger = setup_logger()

@permission_classes([IsAuthenticated])
class AttendenceGetView(ListAPIView):
    """
    API endpoint to retrieve attendance records.
    
    Returns a paginated list of all attendance records.
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    pagination_class = CustomPagination


class AttendenceView(APIView):
    """
    API endpoint for managing attendance records.
    
    Allows teachers to create attendance records and view all attendance.
    """
    permission_classes = ([TeacherPermissions])

    @swagger_auto_schema(
        operation_summary="Create Attendance Record",
        operation_description="Create a new attendance record for students. Teacher access required.",
        request_body=AttendanceSerializer,
        responses={
            201: 'Attendance record created',
            404: 'Teacher not found',
            400: 'Validation error'
        }
    )
    def post(self, request):
        """Create a new attendance record."""
        students = request.data
        
        try:
            # Get teacher from user ID
            teacher_id = Teacher.objects.get(user_id=request.data['teacher_id'])
        except Teacher.DoesNotExist:
            return Response(
                {"error": "Teacher not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        logger.debug('Attendance post data: %s', students)
        logger.info('AttendenceView.post called')

        # Update data with teacher ID
        data = request.data.copy()
        data['teacher_id'] = teacher_id.id
        
        # Create attendance record
        serializer = AttendanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Attendance created by teacher {teacher_id.id}")
            return Response(
                {"message": "Attendance created"},
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        operation_summary="List All Attendance Records",
        operation_description="Retrieve all attendance records. Teacher access required.",
        responses={
            200: openapi.Response('List of attendance records', AttendanceSerializer(many=True)),
            400: 'Error retrieving attendance'
        }
    )
    def get(self, request):
        """Retrieve all attendance records."""
        try:
            at = Attendance.objects.all()
        except Exception as e:
            logger.error(f"Error retrieving attendance: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AttendanceSerializer(at, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class AttendanceDetailView(APIView):
    """
    API endpoint for managing specific attendance records.
    
    Supports updating and deleting attendance records by ID.
    """

    @swagger_auto_schema(
        operation_summary="Update Attendance Record",
        operation_description="Update an existing attendance record. Teacher access required.",
        request_body=AttendanceSerializer,
        responses={
            200: 'Attendance updated',
            404: 'Attendance record not found',
            400: 'Validation error'
        }
    )
    def put(self, request, pk):
        """Update an attendance record."""
        attendance = get_object_or_404(Attendance, pk=pk)
        serializer = AttendanceSerializer(attendance, data=request.data, partial=False)
        
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Attendance {pk} updated")
            return Response({"message": "Attendance updated"}, status=status.HTTP_200_OK)
        
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete Attendance Record",
        operation_description="Delete an attendance record. Teacher access required.",
        responses={
            200: 'Attendance deleted',
            404: 'Attendance record not found'
        }
    )
    def delete(self, request, pk):
        """Delete an attendance record."""
        at = get_object_or_404(Attendance, pk=pk)
        at.delete()
        logger.info(f"Attendance {pk} deleted")
        return Response({"message": "Attendance deleted!"})