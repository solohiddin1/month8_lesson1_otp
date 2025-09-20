from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# from ..serializers import UserSerializer
from app.models.teacher import Teacher
# from app.serializers_f.teacher_serializer import TeacherAddUserSerializer
from app.serializers_f import user_serializer
from app.serializers_f.user_serializer import UserSerializer
from drf_yasg.utils import swagger_auto_schema


from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
import random
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from app.serializers_f.email_serializers import SendEmail, LoginSerializer

@swagger_auto_schema(request_body=LoginSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            otp = random.randint(1000, 9999)
            cache.set(email, otp, timeout=300)

            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}. It is valid for 5 minutes.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response({'success': True, 'message': 'OTP sent to email.'})

        return Response({'success': False, 'message': 'Invalid credentials.'}, status=400)


@swagger_auto_schema(request_body=SendEmail)
@api_view(['POST'])
@permission_classes([AllowAny])
def verify(request):

        email = request.data.get('email')
        otp = request.data.get('otp')

        cached_otp = cache.get(email)
        if cached_otp and str(cached_otp) == str(otp):
            cache.delete(email)

            user = authenticate(request, email=email, password=request.data.get("password"))
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'success': True, 'token': token.key})

            return Response({'success': False, 'message': 'Invalid user.'}, status=400)

        return Response({'success': False, 'message': 'Invalid or expired OTP.'}, status=400)
   

class UserCreateView(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)