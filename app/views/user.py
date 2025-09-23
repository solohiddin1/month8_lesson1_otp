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
from app.models import User

from rest_framework import permissions
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login as django_login



from django.core.mail import send_mail
from django.conf import settings
import random
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from app.serializers_f.email_serializers import SendEmail, LoginSerializer, RegisterSerializer, StudentRegisterSerializer
from app.serializers_f.user_serializer import LoginUserSerializer, ChangePasswordSerializer

@swagger_auto_schema(method='post', request_body=LoginSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
        serializer = LoginSerializer(data=request.data)
        email = request.data.get("email")
        # password = request.data.get("password")

        # user = authenticate(request, email=email, password=password)
        if email is not None:
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


@swagger_auto_schema(method='post',request_body=SendEmail)
@api_view(['POST'])
@permission_classes([AllowAny])
def verify(request):

        seializer = SendEmail(data=request.data)
        seializer.is_valid(raise_exception=True)
        email = seializer.validated_data['email']
        otp = request.data.get('otp')

        cached_otp = cache.get(email)
        if cached_otp and str(cached_otp) == str(otp):
            cache.delete(email)

            user = User.objects.filter(email=email).first()
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'success': True, 'token': token.key})

            return Response({'success': False, 'message': 'Invalid user.'}, status=400)

        return Response({'success': False, 'message': 'Invalid or expired OTP.'}, status=400)
   



@swagger_auto_schema(method='post', request_body=StudentRegisterSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()


    # # Send OTP
    # otp = random.randint(1000, 9999)
    # cache.set(user.email, otp, timeout=300)

    # send_mail(
    #     "Your OTP Code",
    #     f"Your OTP code is {otp}. It is valid for 5 minutes.",
    #     settings.EMAIL_HOST_USER,
    #     [user.email],
    #     fail_silently=False,
    # )
    return Response({"success": True, "message": "User registered successfully."}, status=201)


@swagger_auto_schema(method='post', request_body=LoginUserSerializer)
@api_view(['POST'])
def userlogin(request):
    serializer = LoginUserSerializer(data=request.data)
    print('user here')
    if serializer.is_valid():
        print('user here2 ---')
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        print(email,password,'email password ---')
        
        user = authenticate(request, email=email, password=password)
        if user:
            otp = random.randint(1000, 9999)
            cache.set(email,otp,timeout=300)

            send_mail(
                 "Your code sent",
                    f"Your code is {otp}. It is valid for 5 minutes.",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
            )
            # token, created = Token.objects.get_or_create(user=user)
            return Response({'success': True, 'message': 'OTP sent to email.'})
        return Response({'success': False, 'message': 'Invalid credentials.'}, status=400)
    return Response(serializer.errors, status=400)

@swagger_auto_schema(method='post', request_body=SendEmail)
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_user_email(request):
    serializer = SendEmail(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    otp = request.data.get('otp')

    cached_otp = cache.get(email)
    if cached_otp and str(cached_otp) == str(otp):
        cache.delete(email)

        user = User.objects.filter(email=email).first()
        if user:
            login(request, user)  # Log the user in
            user.is_student = True
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'success': True, 'token': token.key})

        return Response({'success': False, 'message': 'Invalid user.'}, status=400)

    return Response({'success': False, 'message': 'Invalid or expired OTP.'}, status=400)


@swagger_auto_schema(method='post', request_body=LoginUserSerializer)
@api_view(['POST'])
def loginexistinguser(request):
    serializer = LoginUserSerializer(data=request.data)
    print('user here')
    if serializer.is_valid():
        print('user here2 ---')
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        print(email,password,'email password ---')
        
        user = authenticate(request=request._request, email=email, password=password)
        
    
        if user:
            django_login(request._request, user)  # Log the user in
            token, created = Token.objects.get_or_create(user=user)
            return Response({'success': True, 'message': 'user logged in successfully.', 'token': token.key})
        return Response({'success': False, 'message': 'Invalid credentials.'}, status=400)
    return Response(serializer.errors, status=400)


@swagger_auto_schema(method='post', request_body=ChangePasswordSerializer)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not user.check_password(old_password):
        return Response({'success': False, 'message': 'Old password is incorrect.'}, status=400)

    user.set_password(new_password)
    user.save()
    return Response({'success': True, 'message': 'Password changed successfully.'})









class UserCreateView(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)