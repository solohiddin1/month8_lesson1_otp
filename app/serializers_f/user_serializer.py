from rest_framework import serializers
from ..models import User
from rest_framework import serializers
from app.models import User

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



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "phone_number", "password"]

    def create(self, validated_data):
        return User.objects.create_user(
            phone_number=validated_data["phone_number"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
    

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    # fields = ['email', 'password']
        # read_only_fields = ['id', 'email', 'phone_number']

        # To set is_student=True after successful OTP verification, you should update the user's is_student field in your 
        # OTP verification view, not in the serializer.
        # Example (in your OTP verification view):
        # user.is_student = True
        # user.save()
        # In the serializer, you don't need to add is_student here unless you want to display it.
        # If you want to include is_student in the LoginUserSerializer output:
        # is_student = serializers.BooleanField(read_only=True)
    # password = serializers.CharField(write_only=True) 


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)