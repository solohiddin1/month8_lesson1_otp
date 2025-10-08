from rest_framework import serializers
from app.models.homework import Homework, HomeworkUpload 

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        

class HomeworkUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkUpload
        fields = '__all__'
        read_only_fields = ['uploaded_at','updated_at']