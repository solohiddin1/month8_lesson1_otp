from this import d
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from app.models.student import Student
from app.serializers_f.student_serizlizer import StudentSerializer




@permission_classes([IsAuthenticated])
class StudentView(APIView):

    def get(self,request):
        try:
            student = Student.objects.get(user=request.user)
            print(student,'---')
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)
        except Exception as e:
            return Response({"error":str(e)})
        serializer = StudentSerializer(student)
        data = serializer.data.copy()
        data['email'] = student.user.email
        data['phone_number'] = student.user.phone_number
        print(data)
        return Response(data,status=status.HTTP_200_OK)


@permission_classes([IsAdminUser])
class StudentsView(APIView):
    def get(self,request):
        students = Student.objects.all()
        serializer = StudentSerializer(students,many=True)
        print(serializer.data)
        return Response(serializer.data)