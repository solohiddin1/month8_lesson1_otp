from rest_framework import serializers
from ..models import Student
from app.serializers_f.user_serializer import UserSerializer
from app.models import User

class StudentSerializer(serializers.ModelSerializer):   
    user = UserSerializer(required=True)

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student
    

class StudentGetSerializer(serializers.ModelSerializer):   
    # user = UserSerializer(required=True)

    class Meta:
        model = Student
        fields = '__all__'