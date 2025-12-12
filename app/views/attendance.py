from django.shortcuts import get_object_or_404
from drf_yasg.utils import  swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from app.models.attendance import Attendance
from app.models.teacher import Teacher
from app.pagination import CustomPagination
from app.serializers.attendance import AttendanceSerializer
from rest_framework.response import Response
from rest_framework import status
from app.permissions import TeacherPermissions
from log.log import setup_logger

logger = setup_logger()

@permission_classes([IsAuthenticated])
class AttendanceGetView(ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    pagination_class = CustomPagination


class AttendanceView(APIView):
    permission_classes = ([TeacherPermissions])

    @swagger_auto_schema(request_body=AttendanceSerializer)
    def post(self, request):
        students = request.data
        try:
            teacher_id = Teacher.objects.get(user_id=request.data['teacher_id'])
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)
        logger.debug('Attendance post data: %s', students)
        logger.info('AttendanceView.post called')

        data = request.data.copy()
        data['teacher_id'] = teacher_id.id
        serializer = AttendanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Created"},status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        try:
            at = Attendance.objects.all()
        except Exception as e:
            return Response({"error":str(e)})
        serializer = AttendanceSerializer(at,many=True)
        if serializer:
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class AttendanceDetailView(APIView):

    @swagger_auto_schema(request_body=AttendanceSerializer)
    def put(self,request,pk):
        attendance = get_object_or_404(Attendance, pk=pk)
        serializer = AttendanceSerializer(attendance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"updated"},status=status.HTTP_200_OK)
        return Response({"error":serializer.errors})

    def delete(self,request,pk):
        at = get_object_or_404(Attendance, pk=pk)
        at.delete()
        return Response({"message":"attendance deleted!"})