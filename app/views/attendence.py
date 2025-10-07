from pickletools import pystring
from django.shortcuts import get_object_or_404
from drf_yasg.utils import  swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from app.models.attendence import Attendence
from app.models.groups import Group
from app.models.teacher import Teacher
from app.pagination import CustomPagination
from app.serializers_f.attendence import AttendenceSerializer
from rest_framework.response import Response
from rest_framework import status


@permission_classes([IsAuthenticated])
class AttendenceGetView(ListAPIView):
    queryset = Attendence.objects.all()
    serializer_class = AttendenceSerializer
    pagination_class = CustomPagination


class AttendenceView(APIView):
    permission_classes = ([IsAuthenticated])
    @swagger_auto_schema(request_body=AttendenceSerializer)
    def post(self, request):
        # students = request.data
        students = request.data
        teacher_id = Teacher.objects.get(user_id=request.data['teacher_id'])
        # students = request.data.get("attendance",[])
        
        print(students)
        print("requested here---")
        # group_id = students["group_id"]
        
        
        # group = Group.objects.get(pk=group_id)
        # all_students = group.students_set.all()


        data = request.data.copy()
        data['teacher_id'] = teacher_id.id
        serializer = AttendenceSerializer(data=data)
        if serializer.is_valid():
            # for i in all_students:
            #     # Attendence.objects.create(
            #     #     teacher_id = students.teacher_id
            #     # )
            #     Attendence.objects.bulk_create([
            #         Attendence(i) for i in serializer.validated_data
            #     ]
            #     )
            serializer.save()
            return Response({"message":"Created"},status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    # @swagger_auto_schema(request_body=AttendenceSerializer)
    def get(self,request):
        try:
            at = Attendence.objects.all()
        except Exception as e:
            return Response({"error":str(e)})
        serializer = AttendenceSerializer(at,many=True)
        if serializer:
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class AttendanceDetailView(APIView):

    @swagger_auto_schema(request_body=AttendenceSerializer)
    def put(self,request,pk):
        attendance = get_object_or_404(Attendence, pk=pk)
        serializer = AttendenceSerializer(attendance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"updated"},status=status.HTTP_200_OK)
        return Response({"error":serializer.errors})

    def delete(self,request,pk):
        at = get_object_or_404(Attendence, pk=pk)
        at.delete()
        return Response({"message":"attendance deleted!"})