from app.models.groups import Group
from app.models.student import Student
from app.models.teacher import Teacher
from app.serializers_f.group_serializer import GroupSerializer

from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import generics

from app.serializers_f.student_serizlizer import StudentSerializer
from app.views import student



@permission_classes([IsAuthenticated])
class StudentsIngroupView(APIView):

    def get(self,request,pk):
        try:
            group = Group.objects.get(id=pk)
        except Group.DoesNotExist:
            return Response({"error":"Group not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        students = group.students_set.all()
        if students is not None:
            serizlizer = StudentSerializer(students,many=True)
            return Response(serizlizer.data,status=status.HTTP_200_OK)
        return Response({"error":"Nothing"},status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class TeacherGroups(APIView):
    def get(self,request):
        try:
            print(request.user)
            teacher = Teacher.objects.get(user=request.user)
            # for 
            print(teacher.id,teacher.name,)
        except Teacher.DoesNotExist:
            return Response({"error":"Teacher with this id did not found!"},status=status.HTTP_404_NOT_FOUND)
        groups = Group.objects.filter(teacher_id=teacher)

        serializer = GroupSerializer(groups,many=True)
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)



@permission_classes([IsAdminUser])
class AddStudentGroupView(APIView):

    def post(self,request):
        student_id = request.data.get('student_id')
        group_id = request.data.get('group_id')

        try:
            student = Student.objects.get(id=student_id)
            group = Group.objects.get(id=group_id)
            group.students_set.add(student)
            group.student_count = group.students_set.count()
            if not group.is_active and group.student_count>=1:
                group.is_active = True 
            group.save()
            return Response({"message":"Student added successfully"},status=status.HTTP_201_CREATED)
                        
        except Student.DoesNotExist:
            return Response({"error":"Student Not found"},status=status.HTTP_404_NOT_FOUND)


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