from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from app.models.student import Student
from drf_yasg.utils import swagger_auto_schema
from app.serializers_f.attendence import AttendenceSerializer
from app.models.user import User
from app.serializers_f.student_serizlizer import StudentSerializer
from app.serializers_f.group_serializer import GroupSerializer
from app.models.groups import Group



class MockDataView(APIView):
    permission_classes = ([AllowAny])
    
    def get(self, request, year, month):
        year = request.query_params.get('year', year)
        month = request.query_params.get('month', month)

        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({"error": "Invalid year or month"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.all()
        students = Student.objects.filter(user__created_at__year=year,user__created_at__month=month)

        # students = User.objects.filter(created_at__year=year, created_at__month=month)


        serializer = StudentSerializer(students, many=True)
        data = {
            "message": "mock data",
            "status": "success",
            "year": year,
            "month": month,
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class MockDataActiveStudents(APIView):

    def get(self,request):
        students = Student.objects.all()
        groups = Group.objects.all()
        # print(groups)
        # print(students)
        # for i in groups:
        groups_students = groups.first().students_set.all()
        student_serializer = StudentSerializer(students,many=True)
        group_serializer = GroupSerializer(groups,many=True)
        all_students = []
        for g in groups:
            all_students += g.students_set.all()
            print(g.name)
        # print(all_students,'students====')

        # for s in all_students:
        #     print(s.name)

        group_serializer_studnet = StudentSerializer(all_students,many=True)
        # group_serializer_studnet = StudentSerializer(groups_students,many=True)
        
        return Response({"data":group_serializer_studnet.data})

        # return Response({"data":student_serializer.data,"groups":group_serializer.data})