from rest_framework import serializers
from app.models.homework import Homework, HomeworkUpload 

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['id', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class HomeworkUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkUpload
        fields = '__all__'
        read_only_fields = ['uploaded_at','updated_at']


class HomeworkUploadReadSerializer(serializers.ModelSerializer):
    """Serializer for reading homework uploads with nested student data"""
    student = serializers.SerializerMethodField()
    
    class Meta:
        model = HomeworkUpload
        fields = '__all__'
        read_only_fields = ['uploaded_at','updated_at']
    
    def get_student(self, obj):
        """Return student data for display purposes"""
        if obj.student:
            return {
                'id': obj.student.id,
                'name': obj.student.name
            }
        return None