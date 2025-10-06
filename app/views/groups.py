from pydantic.types import _serialize_secret
from django.shortcuts import render
from rest_framework.utils import serializer_helpers
# from app.models import groups
from app.models.groups import Group
from app.models.student import Student
from app.serializers_f.group_serializer import GroupSerializer

from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import generics


class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = GroupSerializer

@permission_classes([IsAuthenticated])
class StudentGroupsView(APIView):

    def get(self,request):
        try:
            student = Student.objects.get(user=request.user)
            groups = student.student_groups.all()
            print(groups)
        except Student.DoesNotExist:
            return Response({"error": "Student not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
            



class GroupCreate(generics.CreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]


class CreateGroupView(APIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=GroupSerializer)
    def post(self,request):
        serializer = GroupSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True,"message":"Group craeted"})
        return Response({"success":False,"errors":serializer.errors},status=400)

    def get(self,request):
        try:
            groups = Group.objects.all()
        except Exception as e:
            return Response({"errors":str(e)})
        
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data,status=200)

    @swagger_auto_schema(request_body=GroupSerializer)
    def put(self,request,pk):
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response({"message":"group not found"},status=404)
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"errors":serializer.errors})

    def delete(self,request,pk):
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response({"error":"Group not found!"},status=status.HTTP_404_NOT_FOUND)
        group.delete()
        return Response({"message":"group deleted successfully"},status=status.HTTP_200_OK) 