from django.core.signals import request_started
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.models.groups import Group
from app.models.homework import Homework
from app.models.student import Student
from app.models.teacher import Teacher
from app.serializers_f import lesson
from app.serializers_f.homework_serializer import HomeworkSerializer
from app.serializers_f.lesson import LessonSerializer

from rest_framework.views import APIView
from app.models.lessons import Lesson
from drf_yasg.utils import status, swagger_auto_schema

# from app.views import teacher


@permission_classes([IsAuthenticated])
class LessonView(APIView):
    # @swagger_auto_schema(request_body=LessonSerializer)
    def post(self, request):
        lessons = request.data
        print(request.data['teacher'],'----')
        teacher_id = Teacher.objects.get(user_id=request.data['teacher'])
        print(lessons)
        data = lessons.copy()
        data['teacher'] = teacher_id.id
        serializer = LessonSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"lesson is created"},status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            lessons = Lesson.objects.all()
            serializer = LessonSerializer(lessons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class LessonDetailView(APIView):
    # @swagger_auto_schema(request_body=LessonSerializer)

    def get(self,request,pk):
        try:
            student = get_object_or_404(Student, user=request.user)
            lesson = get_object_or_404(Lesson, pk=pk, group__students_set=student)
            homework = Homework.objects.filter(lesson=lesson, student=student)
            
            lesson_serializer = LessonSerializer(lesson)
            homework_serializer = HomeworkSerializer(homework)

            return Response({"lesson":lesson_serializer,"homework":homework_serializer})
        except Exception as e:
            print(e)
            return Response({"error":str(e)})

    def put(self, request,pk):
        student = get_object_or_404(Student,user=request.user)
        lesson = get_object_or_404(Lesson,pk=pk,group__students_set=student)
        homework = get_object_or_404(Homework,lesson=lesson,student=student)

        homework_serializer = HomeworkSerializer(homework, data=request.data, partial=True)
        if homework_serializer.is_valid():
            homework_serializer.save()
            return Response({"message":"homework updated"},status=status.HTTP_200_OK)
        return Response({"error":homework_serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request,pk):
    #     lesson = get_object_or_404(Lesson,pk=pk)
    #     # serializer = LessonSerializer(lessons, data=lessons)
    #     if lesson:
    #         lesson.delete()
    #         return Response({"message":"lesson deleted"},status=status.HTTP_200_OK)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)




@permission_classes([IsAuthenticated])
class LessonDetailView(APIView):
    # @swagger_auto_schema(request_body=LessonSerializer)

    def get(self,request,pk):
        try:
            student = get_object_or_404(Student, user=request.user)
            lesson = get_object_or_404(Lesson, pk=pk, group__students_set=student)
            
            lesson_serializer = LessonSerializer(lesson)

            return Response({"lesson":lesson_serializer})
        except Exception as e:
            print(e)
            return Response({"error":str(e)})

    def put(self, request,pk):
        # teacher = get_object_or_404(Teacher,user=request.user)
        # print(teacher.user_id)
        print(request.data,'----data-------')
        print(pk,'pk=-----')
        data = request.data.copy()
        data.update(request.FILES)
        # data._mutable = True
        # files = request.FILES
        lesson = get_object_or_404(Lesson,pk=pk)
        data['teacher'] = lesson.teacher_id
        # lesson = get_object_or_404(Lesson,pk=pk,teacher_id=teacher.user_id)
        print(data,'data======')
        homeworkserializer  = HomeworkSerializer(data=request.data)

        if homeworkserializer.is_valid():
            homework = homeworkserializer.save()
            data['homework'] = homework.id
        print('\n  new data , === ',data)

        clean_data = {k : v[0] if isinstance(v,list) else v for k,v in data.items()}

        homework_serializer = LessonSerializer(lesson, data=clean_data, partial=True)
        if homework_serializer.is_valid():
            homework_serializer.save()
            return Response({"message":"lesson updated"},status=status.HTTP_200_OK)
        return Response({"error":homework_serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):
        lesson = get_object_or_404(Lesson,pk=pk)
        # serializer = LessonSerializer(lessons, data=lessons)
        if lesson:
            lesson.delete()
            return Response({"message":"lesson deleted"},status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)