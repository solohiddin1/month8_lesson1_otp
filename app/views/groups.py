from app.models.groups import Group
from app.models.student import Student
from app.models.teacher import Teacher
from app.serializers_f.group_serializer import GroupSerializer

from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework import generics
from log.log import setup_logger

logger = setup_logger()

from app.serializers_f.student_serizlizer import StudentSerializer
from app.views import student



@permission_classes([IsAuthenticated])
class StudentsIngroupView(APIView):
    """
    API endpoint to retrieve all students in a specific group.
    
    Returns a list of students enrolled in the specified group.
    """

    @swagger_auto_schema(
        operation_summary="Get Students in Group",
        operation_description="Retrieve all students enrolled in a specific group by group ID.",
        responses={
            200: openapi.Response('List of students in the group', StudentSerializer(many=True)),
            404: 'Group not found',
            400: 'Error retrieving students'
        }
    )
    def get(self, request, pk):
        """Retrieve all students in a specific group."""
        try:
            # Get group by ID
            group = Group.objects.get(id=pk)
        except Group.DoesNotExist:
            return Response(
                {"error": "Group not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all students in the group
        students = group.students_set.all()
        if students is not None:
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
            {"error": "No students found"},
            status=status.HTTP_400_BAD_REQUEST
        )


@permission_classes([IsAuthenticated])
class TeacherGroups(APIView):
    """
    API endpoint to retrieve all groups taught by the authenticated teacher.
    
    Returns a list of groups assigned to the currently logged-in teacher.
    """

    @swagger_auto_schema(
        operation_summary="Get Teacher's Groups",
        operation_description="Retrieve all groups assigned to the currently authenticated teacher.",
        responses={
            200: openapi.Response('List of teacher groups', GroupSerializer(many=True)),
            404: 'Teacher not found'
        }
    )
    def get(self, request):
        """Retrieve all groups for the authenticated teacher."""
        try:
            logger.debug('TeacherGroups.get request.user: %s', request.user)
            # Get teacher associated with current user
            teacher = Teacher.objects.get(user=request.user)
            logger.debug('Found teacher id=%s name=%s', teacher.id, teacher.name)
        except Teacher.DoesNotExist:
            return Response(
                {"error": "Teacher with this ID not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get all groups for this teacher
        groups = Group.objects.filter(teacher_id=teacher)

        serializer = GroupSerializer(groups, many=True)
        logger.debug('Teacher groups serializer data: %s', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)



@permission_classes([IsAdminUser])
class AddStudentGroupView(APIView):
    """
    API endpoint to add a student to a group.
    
    Adds a student to a specified group and updates the group's student count.
    Activates the group if it has at least one student. Admin only.
    """

    @swagger_auto_schema(
        operation_summary="Add Student to Group",
        operation_description="Add a student to a group. Updates group count and activation status. Admin only.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['student_id', 'group_id'],
            properties={
                'student_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Student ID'),
                'group_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Group ID')
            }
        ),
        responses={
            201: 'Student added successfully',
            404: 'Student or group not found'
        }
    )
    def post(self, request):
        """Add a student to a group."""
        student_id = request.data.get('student_id')
        group_id = request.data.get('group_id')

        try:
            # Get student and group
            student = Student.objects.get(id=student_id)
            group = Group.objects.get(id=group_id)
            
            # Add student to group
            group.students_set.add(student)
            
            # Update group student count
            group.student_count = group.students_set.count()
            
            # Activate group if it has at least one student
            if not group.is_active and group.student_count >= 1:
                group.is_active = True
            
            group.save()
            logger.info(f"Student {student_id} added to group {group_id}")
            
            return Response(
                {"message": "Student added successfully"},
                status=status.HTTP_201_CREATED
            )
                        
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Group.DoesNotExist:
            return Response(
                {"error": "Group not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class GroupListView(generics.ListAPIView):
    """
    API endpoint to list all groups.
    
    Returns a list of all groups in the system. Admin only.
    """
    queryset = Group.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = GroupSerializer

    @swagger_auto_schema(
        operation_summary="List All Groups",
        operation_description="Retrieve a list of all groups. Admin access required.",
        responses={
            200: openapi.Response('List of all groups', GroupSerializer(many=True))
        }
    )

@permission_classes([IsAuthenticated])
class StudentGroupsView(APIView):
    """
    API endpoint to retrieve all groups for the authenticated student.
    
    Returns a list of groups the currently logged-in student is enrolled in.
    """

    @swagger_auto_schema(
        operation_summary="Get Student's Groups",
        operation_description="Retrieve all groups the currently authenticated student is enrolled in.",
        responses={
            200: openapi.Response('List of student groups', GroupSerializer(many=True)),
            404: 'Student not found',
            400: 'Error retrieving groups'
        }
    )
    def get(self, request):
        """Retrieve all groups for the authenticated student."""
        try:
            # Get student associated with current user
            student = Student.objects.get(user=request.user)
            # Get all groups for this student
            groups = student.student_groups.all()
            logger.debug('Student groups for user %s: %s', request.user, groups)
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
            



class GroupCreate(generics.CreateAPIView):
    """
    API endpoint to create a new group.
    
    Creates a new group in the system. Admin only.
    """
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Create Group",
        operation_description="Create a new group. Admin access required.",
        responses={
            201: openapi.Response('Group created successfully', GroupSerializer),
            400: 'Validation error'
        }
    )

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, or deleting a specific group.
    
    Supports GET (retrieve), PUT/PATCH (update), and DELETE operations. Admin only.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Get Group Details",
        operation_description="Retrieve detailed information about a specific group. Admin only.",
        responses={
            200: openapi.Response('Group details', GroupSerializer),
            404: 'Group not found'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Group",
        operation_description="Update a group's information. Admin only.",
        responses={
            200: openapi.Response('Group updated successfully', GroupSerializer),
            404: 'Group not found',
            400: 'Validation error'
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update Group",
        operation_description="Partially update a group's information. Admin only.",
        responses={
            200: openapi.Response('Group updated successfully', GroupSerializer),
            404: 'Group not found',
            400: 'Validation error'
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Group",
        operation_description="Delete a group. Admin only.",
        responses={
            204: 'Group deleted successfully',
            404: 'Group not found'
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CreateGroupView(APIView):
    """
    API endpoint for managing groups (CRUD operations).
    
    Supports creating, listing, updating, and deleting groups.
    Note: This view duplicates functionality in GroupCreate and GroupDetailView.
    Consider using those views instead for better separation of concerns.
    """
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create Group (Legacy)",
        operation_description="Create a new group. Consider using GroupCreate endpoint instead.",
        request_body=GroupSerializer,
        responses={
            200: openapi.Response('Group created successfully', GroupSerializer),
            400: 'Validation error'
        }
    )
    def post(self, request):
        """Create a new group."""
        serializer = GroupSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            logger.info("Group created successfully")
            return Response({"success": True, "message": "Group created"})
        return Response({"success": False, "errors": serializer.errors}, status=400)

    @swagger_auto_schema(
        operation_summary="List All Groups (Legacy)",
        operation_description="Retrieve all groups. Consider using GroupListView endpoint instead.",
        responses={
            200: openapi.Response('List of all groups', GroupSerializer(many=True))
        }
    )
    def get(self, request):
        """Retrieve all groups."""
        try:
            groups = Group.objects.all()
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        operation_summary="Update Group (Legacy)",
        operation_description="Update a group. Consider using GroupDetailView endpoint instead.",
        request_body=GroupSerializer,
        responses={
            200: openapi.Response('Group updated successfully', GroupSerializer),
            404: 'Group not found',
            400: 'Validation error'
        }
    )
    def put(self, request, pk):
        """Update a group."""
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response({"message": "Group not found"}, status=404)
        
        # Fix: Update existing group instead of creating new one
        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Group {pk} updated successfully")
            return Response(serializer.data)
        return Response({"errors": serializer.errors}, status=400)

    @swagger_auto_schema(
        operation_summary="Delete Group (Legacy)",
        operation_description="Delete a group. Consider using GroupDetailView endpoint instead.",
        responses={
            200: 'Group deleted successfully',
            404: 'Group not found'
        }
    )
    def delete(self, request, pk):
        """Delete a group."""
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response(
                {"error": "Group not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        group.delete()
        logger.info(f"Group {pk} deleted successfully")
        return Response(
            {"message": "Group deleted successfully"},
            status=status.HTTP_200_OK
        ) 