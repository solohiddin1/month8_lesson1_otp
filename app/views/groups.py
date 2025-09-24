from operator import truediv
import stat
from sys import exception
from termios import IOCSIZE_MASK
from pydantic.types import _serialize_secret
from django.shortcuts import render
from app.models import groups
from app.models.groups import Group
from app.serializers_f.group_serializer import GroupSerializer

from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

class CreateGroupView(APIView):
    serializer_classes = GroupSerializer
    permission_classes = [AllowAny]

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

    def put(self,request):
        pass

    def delete(self,request):
        pass