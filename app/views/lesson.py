from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from app.serializers_f.lesson import LessonSerializer

from rest_framework.views import APIView
from app.models.lessons import Lesson
from drf_yasg.utils import status, swagger_auto_schema

class LessonView(APIView):
    @swagger_auto_schema(request_body=LessonSerializer)
    def post(self, request):
        lessons = request.data
        serializer = LessonSerializer(data=lessons)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"created lesson"},status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            lessons = Lesson.objects.all()
            serializer = LessonSerializer(lessons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LessonDetailView(APIView):
    @swagger_auto_schema(request_body=LessonSerializer)
    def put(self, request,pk):
        lessons = get_object_or_404(Lesson,pk=pk)
        serializer = LessonSerializer(lessons, data=lessons)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"lesson updated"},status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):
        lesson = get_object_or_404(Lesson,pk=pk)
        # serializer = LessonSerializer(lessons, data=lessons)
        if lesson:
            lesson.delete()
            return Response({"message":"lesson deleted"},status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
