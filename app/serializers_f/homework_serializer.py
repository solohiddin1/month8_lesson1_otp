from rest_framework import serializers
from app.models.homework import Homework 

class HomeworkSerializer(serializers.Serializer):
    class Meta:
        model = Homework
        fields = '__all__'
        read_only_fields = ['uploaded_at','updated_at']