from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from app.models.student import Student
from drf_yasg.utils import swagger_auto_schema
from app.serializers_f.attendence import AttendenceSerializer
from app.models.user import User

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

        students = User.objects.filter(created_at__year=year, created_at__month=month)



        serializer = AttendenceSerializer(students, many=True)
        data = {
            "message": "This is mock data",
            "status": "success",
            "year": year,
            "month": month,
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    