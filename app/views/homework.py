from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView, permission_classes
from rest_framework.permissions import IsAuthenticated
from app.models.homework import Homework, HomeworkUpload
from rest_framework.response import Response
from app.models.student import Student
from app.serializers_f.homework_serializer import HomeworkSerializer, HomeworkUploadSerializer


@permission_classes([IsAuthenticated])
class HomeworkUploadView(APIView):
    
    def post(self, request):
        # pk = request.data.get('id')
        print(request.data)
        try:
            student = Student.objects.get(user=request.data['student'])
        except Student.DoesNotExist:
            return Response({"error":"student not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        data['student'] = student.id
        serializer = HomeworkUploadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Homework saved"}, status=201)
        return Response({"error": serializer.errors}, status=400)



@permission_classes([IsAuthenticated])
class HomeworkPutMarkView(APIView):

    def post(self, request,pk):
        # pk = request.data.get('id')
        print(request.data)
        if not pk:
            return Response({"error": "Homework ID is required"}, status=400)
        try:
            homework = HomeworkUpload.objects.get(pk=pk)
        except HomeworkUpload.DoesNotExist:
            return Response({"error": "Homework not found"}, status=404)
        print(homework.is_checked)
        homework.is_checked = True
        
        serializer = HomeworkUploadSerializer(homework, data=request.data, partial=True)
        if serializer.is_valid():
            
            serializer.save()
            return Response({"message": "Homework updated"}, status=200)
        return Response({"error": serializer.errors}, status=400)


@permission_classes([IsAuthenticated])
class HomeworkView(APIView):


    def post(self, request):
        serializer = HomeworkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Homework created"}, status=201)
        return Response({"error": serializer.errors}, status=400)


    def get(self, request):
        homeworks = HomeworkUpload.objects.all()
        serializer = HomeworkUploadSerializer(homeworks, many=True)
        return Response(serializer.data, status=200)


class HomeworkDetailView(APIView):

    def post(self, request,pk):
        serializer = HomeworkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Homework created"}, status=201)
        return Response({"error": serializer.errors}, status=400)

    def put(self, request,pk):
        # pk = request.data.get('id')
        print(request.data)
        if not pk:
            return Response({"error": "Homework ID is required"}, status=400)
        try:
            homework = Homework.objects.get(pk=pk)
        except Homework.DoesNotExist:
            return Response({"error": "Homework not found"}, status=404)
        serializer = HomeworkSerializer(homework, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Homework updated"}, status=200)
        return Response({"error": serializer.errors}, status=400)