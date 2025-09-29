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
