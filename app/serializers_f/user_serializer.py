from rest_framework import serializers
from ..models import User

class UserSerializer(serializers.ModelSerializer):   
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['is_teacher','is_admin','is_student','created_at','updated_at']

    def create(self, validated_data):
        validated_data['is_teacher'] = True
        validated_data['is_admin'] = False
        validated_data['is_student'] = False
        return super().create(validated_data)