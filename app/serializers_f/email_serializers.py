from rest_framework import serializers
# from models.user import User

class SendEmail(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
