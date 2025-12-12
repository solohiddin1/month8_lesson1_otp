from rest_framework import serializers

from app.models.attendance import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["teacher_id", "group_id", "lesson", "absent_students"]