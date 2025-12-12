from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.status import HTTP_400_BAD_REQUEST
from app.serializers.user_serializer import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from app.models import User
from rest_framework import permissions
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login as django_login
from django.core.mail import send_mail
from django.conf import settings
import random
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from app.serializers.email_serializers import SendEmail, LoginSerializer
from app.serializers.user_serializer import LoginUserSerializer, ChangePasswordSerializer
# from app.serializers.student_serializer import StudentSerializer
from log.log import setup_logger

logger = setup_logger()


class LoginAPIView(generics.GenericAPIView):
    """
    API endpoint for user login via OTP.
    
    Sends a one-time password (OTP) to the user's email address.
    The OTP is valid for 5 minutes and stored in cache.
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Login via OTP",
        operation_description="Send OTP to user's email for authentication. OTP is valid for 5 minutes.",
        responses={
            200: openapi.Response('OTP sent successfully', LoginSerializer),
            400: 'Invalid email or request'
        }
    )
    def post(self, request, *args, **kwargs):
        """Send OTP to user's email for login."""
        serializer = self.get_serializer(data=request.data)
        email = request.data.get("email")

        if email is not None:
            # Generate 4-digit OTP
            otp = random.randint(1000, 9999)
            # Cache OTP with 5-minute expiration
            cache.set(email, otp, timeout=300)

            # Send OTP via email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}. It is valid for 5 minutes.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            logger.info(f"OTP sent to {email}")
            return Response({'success': True, 'message': 'OTP sent to email.'})
        
        logger.warning(f"Login attempt with invalid email: {email}")
        return Response({'success': False, 'message': 'Invalid credentials.'}, status=400)


class VerifyOTPAPIView(generics.GenericAPIView):
    """
    API endpoint to verify OTP and authenticate user.
    
    Validates the OTP sent to user's email and returns JWT tokens upon success.
    """
    serializer_class = SendEmail
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Verify OTP",
        operation_description="Verify the OTP code sent to user's email and receive JWT tokens.",
        responses={
            200: openapi.Response('OTP verified successfully, returns JWT tokens'),
            400: 'Invalid or expired OTP'
        }
    )
    def post(self, request, *args, **kwargs):
        """Verify OTP and return JWT tokens."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        otp = request.data.get('otp')

        # Check if OTP matches cached value
        cached_otp = cache.get(email)
        if cached_otp and str(cached_otp) == str(otp):
            # Clear OTP from cache after successful verification
            cache.delete(email)

            user = User.objects.filter(email=email).first()
            if user:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                logger.info(f"User {email} verified successfully")
                return Response({
                    'success': True, 
                    'access': str(refresh.access_token), 
                    'refresh': str(refresh)
                })

            logger.warning(f"OTP verified but user not found: {email}")
            return Response({'success': False, 'message': 'Invalid user.'}, status=400)

        logger.warning(f"Invalid or expired OTP for {email}")
        return Response({'success': False, 'message': 'Invalid or expired OTP.'}, status=400)
   

def userlogin_view(request):
    return render(request,'login.html')


class UserLogin(generics.GenericAPIView):
    """
    API endpoint for user login with OTP.
    
    Accepts both JSON and form data. Sends OTP to user's email upon successful authentication.
    """
    serializer_class = LoginUserSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="User Login with OTP",
        operation_description="Login user with email and password. Sends OTP to email if credentials are valid.",
        responses={
            200: openapi.Response('OTP sent to email'),
            400: 'Invalid credentials or validation error'
        }
    )
    def post(self, request, *args, **kwargs):
        """Authenticate user and send OTP to email."""
        # Handle both JSON and form data
        if request.content_type == 'application/json':
            data = request.data
        else:
            data = {
                'email': request.POST.get('email'),
                'password': request.POST.get('password')
            }
        
        serializer = self.get_serializer(data=data)
        logger.info("UserLogin.post called")
        
        if serializer.is_valid():
            logger.info('Login serializer is valid')
            email = serializer.validated_data.get("email", "").strip().lower()
            password = serializer.validated_data.get("password", "").strip()
            
            # Do not log passwords
            logger.info("Attempting login for email=%s", email)
            
            # Authenticate user
            user = authenticate(request, email=email, password=password)
            logger.debug("authenticate returned: %s", user)
            
            if user:
                # Generate and cache OTP
                otp = random.randint(1000, 9999)
                cache.set(email, otp, timeout=300)
                
                logger.info("Sending OTP email to %s", email)
                # Send OTP via email
                send_mail(
                    "Your code sent",
                    f"Your code is {otp}. It is valid for 5 minutes.",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                
                return Response(
                    {'success': True, 'message': 'OTP sent to email.'},
                    status=status.HTTP_200_OK
                )
            
            logger.warning(f"Invalid credentials for email: {email}")
            return Response(
                {'success': False, 'message': 'Invalid credentials.'}, 
                status=400
            )
        
        return Response(serializer.errors, status=400)

def verify_user_email_view(request):
    return render(request,'verify_otp.html')

class VerifyUserEmailAPIView(generics.GenericAPIView):
    """
    API endpoint to verify user's email with OTP.
    
    Validates the OTP and marks the user's email as verified.
    Returns JWT tokens upon successful verification.
    """
    serializer_class = SendEmail
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Verify User Email",
        operation_description="Verify user's email using OTP and mark email as verified. Returns JWT tokens.",
        responses={
            200: openapi.Response('Email verified successfully, returns JWT tokens'),
            400: 'Invalid or expired OTP'
        }
    )
    def post(self, request, *args, **kwargs):
        """Verify user's email with OTP and return JWT tokens."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = request.data.get('otp')

        cached_otp = cache.get(email)
        logger.debug("Cached OTP for %s: %s", email, cached_otp)
        logger.info('verify_user_email called for %s', email)
        
        if cached_otp and str(cached_otp) == str(otp):
            logger.debug("OTP matched for %s (deleting cache)", email)
            # Clear OTP from cache
            cache.delete(email)

            user = User.objects.filter(email=email).first()
            if user:
                # Mark email as verified
                user.email_verified = True
                user.save()
                
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                logger.info(f"Email verified for user: {email}")
                return Response({
                    'success': True, 
                    'message': 'Email verification successful', 
                    'access': str(refresh.access_token), 
                    'refresh': str(refresh)
                })

            logger.warning(f"OTP valid but user not found: {email}")
            return Response({'success': False, 'message': 'Invalid user.'}, status=400)

        logger.warning(f"Invalid or expired OTP for email verification: {email}")
        return Response({'success': False, 'message': 'Invalid or expired OTP.'}, status=400)

class LogoutAPIView(generics.GenericAPIView):
    """
    API endpoint for user logout.
    
    Blacklists the refresh token to invalidate the user's session.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="User Logout",
        operation_description="Logout user by blacklisting the refresh token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token to blacklist')
            }
        ),
        responses={
            200: openapi.Response('Logged out successfully'),
            400: 'Refresh token required or invalid'
        }
    )
    def post(self, request, *args, **kwargs):
        """Logout user by blacklisting refresh token."""
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                logger.warning("Logout attempt without refresh token")
                return Response(
                    {"success": False, "error": "Refresh token required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("User logged out successfully")
            return Response({"success": True, "message": "Logged out successfully"})
        except Exception as exc:
            logger.error(f"Logout error: {str(exc)}")
            return Response(
                {"success": False, "error": str(exc)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class ChangePasswordAPIView(generics.GenericAPIView):
    """
    API endpoint for changing user password.
    
    Requires email verification and validates old password before setting new password.
    Returns JWT tokens upon successful password change.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Change Password",
        operation_description="Change user password by providing email, old password, and new password. Email must be verified.",
        responses={
            200: openapi.Response('Password changed successfully, returns JWT tokens'),
            400: 'Invalid credentials or validation error'
        }
    )
    def post(self, request, *args, **kwargs):
        """Change user password and return JWT tokens."""
        logger.info('change_password called')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']
        
        # Avoid logging raw passwords
        logger.info('Password change requested for %s', email)

        try:
            user1 = User.objects.get(email=email)
        except Exception as e:
            logger.exception('Error fetching user for email %s', email)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        logger.debug('Fetched user: %s', user1)
        
        # Validate password constraints
        if old_password == new_password:
            return Response(
                {"message": "Please enter a new password different from the old one"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_password != confirm_password:
            return Response(
                {"message": "New password and confirm password must match!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate user with old password
        user = authenticate(request._request, email=email, password=old_password)
        logger.debug('authenticate returned: %s', user)
        
        if user is None:
            return Response(
                {"error": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info('User authenticated for password change: %s', email)
        
        # Check email verification
        if not user1.email_verified:
            return Response(
                {'success': False, 'message': 'Email not verified'}, 
                status=HTTP_400_BAD_REQUEST
            )
        
        # Update password
        user.set_password(new_password)
        user.is_active = True
        user.save()
        
        # Login user and generate tokens
        django_login(request._request, user)
        refresh = RefreshToken.for_user(user)
        
        logger.info(f"Password changed successfully for {email}")
        return Response({
            'success': True, 
            'message': 'Password changed successfully.', 
            'access': str(refresh.access_token), 
            'refresh': str(refresh)
        })

@permission_classes(IsAuthenticated)
def change_password_page(request):

    return render(request,'change_password.html')


# @swagger_auto_schema(method='post', request_body=LoginSerializer)
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def forgot_password(request):
    serializer = LoginSerializer(data=request.data)
    logger.debug('forgot_password serializer data: %s', request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=serializer.validated_data['email'])
        except Exception as e:
            return Response({"error":str(e)})
        if user:
            otp = random.randint(1000,9999)
            cache.set(email,otp,timeout=300)
            logger.info("OTP sent to %s for forgot_password", email)
            send_mail(
                 "Your code sent",
                    f"Your code is {otp}. It is valid for 5 minutes.",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                    )
            return Response({"message":"please verify your email, we sent code to your email"}) 
        return Response({"error":"User not found"})
    return Response({"error":serializer.errors})





# from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from app.utils import generate_reset_password_link

token_generator = PasswordResetTokenGenerator()

def forgot_password_view(request):
    return render(request,'forgot_password.html')

class ForgotPasswordAPIView(generics.GenericAPIView):
    """
    API endpoint for password reset request.
    
    Sends a password reset link to the user's email address.
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Forgot Password",
        operation_description="Request password reset link. Link will be sent to user's email.",
        responses={
            200: openapi.Response('Reset link sent successfully'),
            404: 'User not found'
        }
    )
    def post(self, request, *args, **kwargs):
        """Send password reset link to user's email."""
        email = request.data.get("email")
        
        try:
            user = User.objects.get(email=email)
            # Generate password reset link
            reset_link = generate_reset_password_link(user, request)
            
            # Send reset link via email
            send_mail(
                "Reset your password",
                f"Your reset password link: {reset_link}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            
            logger.info(f"Password reset link sent to {email}")
            return Response({"reset_link": reset_link})
        except User.DoesNotExist:
            logger.warning(f"Password reset requested for non-existent user: {email}")
            return Response({"error": "User not found"}, status=404)

from rest_framework import serializers

class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for password reset."""
    password = serializers.CharField(write_only=True, help_text="New password")


class ResetPasswordAPIView(generics.GenericAPIView):
    """
    API endpoint for resetting password using token.
    
    Validates the reset token and updates user's password.
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Reset Password",
        operation_description="Reset user password using the token from reset link.",
        responses={
            200: openapi.Response('Password reset successful'),
            400: 'Invalid or expired token'
        }
    )
    def post(self, request, uidb64, token, *args, **kwargs):
        """Reset password using token."""
        try:
            # Decode user ID from base64
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            logger.debug('reset_password link for user: %s email:%s', user, user.email)
        except Exception:
            logger.warning("Invalid reset password link")
            return Response({"error": "Invalid link"}, status=400)

        # Validate token
        if token_generator.check_token(user, token):
            new_password = request.data.get("password")
            
            # Update password
            user.set_password(new_password)
            user.save()
            
            logger.info(f"Password reset successful for user: {user.email}")
            return Response({
                "message": "Password reset successful",
                "password": new_password
            })
        
        logger.warning(f"Invalid or expired token for user: {user.email}")
        return Response({"error": "Invalid or expired token"}, status=400)


def reset_page(request,uiid64,token):
    if request.method == 'POST':
        password = request.POST.get("password")
        conf_password = request.POST.get("conf_password")

        if password != conf_password:
            return render(request,'reset_password.html',{
                "error":"passwords dont match",
                "uiid64":uiid64,
                "token":token
                }
            )
        try:
            uid = urlsafe_base64_decode(uiid64).decode()
            user = User.objects.get(pk=uid)
        except Exception as e:
            return render(request,'reset_password.html',{"error":"Invalid link"})

        if default_token_generator.check_token(user,token):
            user.set_password(conf_password)
            user.save()
            return redirect('home')
        else:
            return render(request,'reset_password.html',{"error":"Token expired"})
        
    return render(request,'reset_password.html',{"uiid64":uiid64,"token":token})


# @permission_classes(IsAuthenticated)
from django.contrib.auth.decorators import login_required

# @login_required
# @login_required(login_url='/userlogin/')

# @api_view(["GET"])
@permission_classes([IsAuthenticated])
def home(request):
    return render(request,"home.html")

def loginexistinguser_view(request):
    return render(request,'loginexisting.html')
    

@permission_classes([IsAuthenticated])
def student_dashboard(request):
    return render(request,'student_dashboard.html')


class LoginExistingUserAPIView(generics.GenericAPIView):
    """
    API endpoint for existing user login.
    
    Authenticates existing users with email and password.
    Requires email verification. Returns JWT tokens with user role.
    """
    serializer_class = LoginUserSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Login Existing User",
        operation_description="Login for existing users with verified email. Returns JWT tokens with role information.",
        responses={
            200: openapi.Response('Login successful, returns JWT tokens'),
            400: 'Invalid credentials or email not verified',
            404: 'User not found'
        }
    )
    def post(self, request, *args, **kwargs):
        """Authenticate existing user and return JWT tokens."""
        serializer = self.get_serializer(data=request.data)
        logger.info('loginexistinguser called')
        
        if serializer.is_valid():
            logger.info('loginexistinguser serializer valid')
            email = serializer.validated_data.get("email", "").strip().lower()
            
            try:
                userin = User.objects.get(email=email)
            except User.DoesNotExist:
                logger.warning(f"Login attempt for non-existent user: {email}")
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            password = serializer.validated_data.get("password", "").strip()
            logger.info('Attempting existing login for email=%s', email)
            
            # Authenticate user
            user = authenticate(request=request._request, email=email, password=password)
            logger.debug('authenticate returned: %s', user)
            logger.debug('userin: %s', userin)
            
            if user is None:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check email verification
            if not userin.email_verified:
                return Response(
                    {"error": "Email is not verified"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Login user and generate tokens
            django_login(request._request, user)
            refresh = RefreshToken.for_user(user)
            
            # Determine user role
            role = (
                'admin' if userin.is_admin else 
                'teacher' if userin.is_teacher else 
                'student' if userin.is_student else 
                'User'
            )
            refresh['role'] = role
            
            logger.info('User %s logged in with role %s', email, role)
            logger.debug('Refresh token info: %s', refresh)
            
            return Response({
                'success': True,
                'message': 'User logged in successfully.',
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })

        return Response(serializer.errors, status=400)