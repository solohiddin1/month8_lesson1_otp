from rest_framework import serializers

from app.models.attendence import Attendence


class AttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendence
        fields = '__all__'