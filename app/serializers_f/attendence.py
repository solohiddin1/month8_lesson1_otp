from rest_framework import serializers

from app.models.attendence import Attendence


class AttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendence
        fields = ["teacher_id", "group_id","lesson","absent_students"]