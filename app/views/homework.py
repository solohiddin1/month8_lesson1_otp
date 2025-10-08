from rest_framework.decorators import APIView, permission_classes
from rest_framework.permissions import IsAuthenticated
from app.models.homework import Homework
from rest_framework.response import Response
from app.serializers_f.homework_serializer import HomeworkSerializer

@permission_classes([IsAuthenticated])
class HomeworkView(APIView):


    def post(self, request):
        serializer = HomeworkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Homework created"}, status=201)
        return Response({"error": serializer.errors}, status=400)


    def get(self, request):
        homeworks = Homework.objects.all()
        serializer = HomeworkSerializer(homeworks, many=True)
        return Response(serializer.data, status=200)


class HomeworkDetailView(APIView):

    def post(self, request,pk):
        serializer = HomeworkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Homework created"}, status=201)
        return Response({"error": serializer.errors}, status=400)

    def put(self, request):
        pk = request.data.get('id')
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