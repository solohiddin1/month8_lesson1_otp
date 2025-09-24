from colorsys import TWO_THIRD
from pdb import Restart
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# from ..serializers import UserSerializer
from app.models import teacher
from app.models.teacher import Teacher
from app.serializers_f.teacher_serializer import TeacherAddUserSerializer, TeacherSerializer
from drf_yasg.utils import swagger_auto_schema

class TeacherCreateView(APIView):
    @swagger_auto_schema(request_body=TeacherAddUserSerializer)
    def post(self,request):

        serializer = TeacherAddUserSerializer(data=request.data)
        if serializer.is_valid():
            teacher = serializer.save()
            return Response(TeacherSerializer(teacher).data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        
        teachers = Teacher.objects.all()
        if teachers:
            serializer = TeacherSerializer(teachers,many=True)
            return Response(serializer.data,status=200)
        return Response({"error ": serializer.errors},status=404)

    def put(self):
        pass

    def delete(self):
        pass