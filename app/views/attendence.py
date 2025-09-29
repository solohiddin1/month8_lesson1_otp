from drf_yasg.utils import  swagger_auto_schema
from rest_framework.decorators import APIView
from app.models.attendence import Attendence
from app.serializers_f.attendence import AttendenceSerializer
from rest_framework.response import Response
from rest_framework import status

class AttendenceView(APIView):
    @swagger_auto_schema(request_body=AttendenceSerializer)
    def post(self, request):
        # students = request.data
        students = request.data.get("attendance",[])
        print(students)

        serializer = AttendenceSerializer(data=students,many=True)
        if serializer.is_valid():
            Attendence.objects.bulk_create([
                Attendence(**i) for i in serializer.validated_data
            ]
            )
            return Response({"message":"Created"},status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

