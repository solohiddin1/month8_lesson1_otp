from rest_framework import serializers
from app.models.homework import Homework, HomeworkUpload 

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['id', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class HomeworkUploadSerializer(serializers.ModelSerializer):
    # Nested serializers to include student and homework details
    student = serializers.SerializerMethodField()
    homework = HomeworkSerializer(read_only=True)
    
    class Meta:
        model = HomeworkUpload
        fields = '__all__'
        read_only_fields = ['uploaded_at','updated_at']
    
    def get_student(self, obj):
        """Return student details including name."""
        if obj.student:
            return {
                'id': obj.student.id,
                'name': obj.student.name
            }
        return None