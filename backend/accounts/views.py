from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import CustomUser
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import COUNTRY
from .serializers import CountrySerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.settings import api_settings
from rest_framework.permissions import AllowAny

class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access
    
    def post(self, request):
        print("==== Login Request ====")
        print(f"Request Data: {request.data}")
        print(f"Request Headers: {request.headers}")
        print(f"Request Method: {request.method}")
        print(f"Request Path: {request.path}")
        
        user_id = request.data.get('user_id')
        password = request.data.get('password')

        if not user_id or not password:
            print(f"Missing credentials - user_id: {bool(user_id)}, password: {bool(password)}")
            return Response({
                'status': 'error',
                'message': 'Please provide both USER_ID and PASSWORD'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            print(f"Looking for user with ID: {user_id.upper()}")
            user = CustomUser.objects.get(USER_ID=user_id.upper())
            
            print(f"Login attempt for user: {user.USER_ID}")
            print(f"Failed attempts: {user.FAILED_LOGIN_ATTEMPTS}")
            print(f"Last failed login: {user.LAST_FAILED_LOGIN}")
            print(f"Permanent lock: {user.PERMANENT_LOCK}")

            if not user.IS_ACTIVE:
                return Response({
                    'status': 'error',
                    'message': 'Account is not active'
                }, status=status.HTTP_403_FORBIDDEN)

            # Check account lock status
            is_locked, lock_message = user.is_account_locked()
            if is_locked:
                return Response({
                    'status': 'error',
                    'message': lock_message
                }, status=status.HTTP_403_FORBIDDEN)

            # Verify password
            if not user.check_password(password):
                user.increment_failed_attempts()
                
                remaining_attempts = 0
                if user.FAILED_LOGIN_ATTEMPTS < 3:
                    remaining_attempts = 3 - user.FAILED_LOGIN_ATTEMPTS
                elif user.FAILED_LOGIN_ATTEMPTS < 5:
                    remaining_attempts = 5 - user.FAILED_LOGIN_ATTEMPTS
                elif user.FAILED_LOGIN_ATTEMPTS < 8:
                    remaining_attempts = 8 - user.FAILED_LOGIN_ATTEMPTS
                
                message = "Invalid credentials. "
                if remaining_attempts > 0:
                    message += f"{remaining_attempts} attempts remaining before next level of account lock."
                else:
                    message += "Account will be locked due to too many failed attempts."
                
                return Response({
                    'status': 'error',
                    'message': message
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Reset failed attempts on successful login
            user.reset_failed_attempts()

            # Generate and send OTP
            otp = user.generate_otp()
            
            try:
                send_mail(
                    subject='Login Verification OTP - College ERP',
                    message=(
                        f'Dear {user.FIRST_NAME},\n\n'
                        f'Your verification OTP is: {otp}\n'
                        f'This OTP will expire in 3 minutes.\n\n'
                        f'If you did not attempt to login, please secure your account.\n\n'
                        f'Best regards,\n'
                        f'College ERP Team'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.EMAIL],
                    fail_silently=False,
                )
                
                return Response({
                    'status': 'success',
                    'message': 'Login successful. Please verify OTP sent to your email.',
                    'user_id': user.USER_ID,
                    'email': user.EMAIL[:3] + '*' * (len(user.EMAIL.split('@')[0]) - 3) + '@' + user.EMAIL.split('@')[1]
                }, status=status.HTTP_200_OK)
                
            except Exception as e:
                user.OTP_SECRET = None
                user.save()
                return Response({
                    'status': 'error',
                    'message': 'Failed to send verification OTP. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except CustomUser.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Invalid USER_ID'
            }, status=status.HTTP_404_NOT_FOUND)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class SendOTPView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access
    
    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({
                'status': 'error',
                'message': 'Please provide USER_ID'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(USER_ID=user_id)
            
            if not user.IS_ACTIVE:
                return Response({
                    'status': 'error',
                    'message': 'Account is not active'
                }, status=status.HTTP_403_FORBIDDEN)
 
            # Check account lock status and get detailed message
            is_locked, lock_message = user.is_account_locked()
            if is_locked:
                return Response({
                    'status': 'error',
                    'message': lock_message,
                    'locked': True,
                    'lockTime': user.LOCK_EXPIRY.isoformat() if user.LOCK_EXPIRY else None
                }, status=status.HTTP_403_FORBIDDEN)

            otp = user.generate_otp()
            
            try:
                send_mail(
                    subject='Login OTP - College ERP',
                    message=(
                        f'Dear {user.FIRST_NAME},\n\n'
                        f'Your OTP for login is: {otp}\n'
                        f'This OTP will expire in 3 minutes.\n\n'
                        f'If you did not request this OTP, please ignore this email.\n\n'
                        f'Best regards,\n'
                        f'College ERP Team'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.EMAIL],
                    fail_silently=False,
                )
                
                return Response({
                    'status': 'success',
                    'message': f'OTP sent successfully to {user.EMAIL}',
                    'user_id': user.USER_ID,
                    'email': user.EMAIL[:3] + '*' * (len(user.EMAIL.split('@')[0]) - 3) + '@' + user.EMAIL.split('@')[1]
                }, status=status.HTTP_200_OK)
                
            except Exception as e:
                user.OTP_SECRET = None
                user.save()
                return Response({
                    'status': 'error',
                    'message': 'Failed to send OTP email. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except CustomUser.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Invalid USER_ID'
            }, status=status.HTTP_404_NOT_FOUND)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access
    
    def post(self, request):
        user_id = request.data.get('user_id')
        otp = request.data.get('otp')
        
        if not user_id or not otp:
            return Response({
                'status': 'error',
                'message': 'Both user_id and OTP are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(USER_ID=user_id)
            is_valid, message = user.verify_otp(otp)
            
            if is_valid:
                # Update login info
                user.update_login_info(request.META.get('REMOTE_ADDR'))
                
                # Generate tokens manually
                refresh = RefreshToken()
                refresh[api_settings.USER_ID_CLAIM] = user.USER_ID
                refresh['user_id'] = user.USER_ID  # Add custom claims
                refresh['username'] = user.USERNAME
                refresh['is_superuser'] = user.IS_SUPERUSER
                
                return Response({
                    'status': 'success',
                    'message': message,
                    'token': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': {
                        'user_id': user.USER_ID,
                        'username': user.USERNAME,
                        'email': user.EMAIL,
                        'designation': {
                            'code': user.DESIGNATION.CODE,
                            'name': user.DESIGNATION.NAME,
                        },
                        'first_name': user.FIRST_NAME,
                        'last_name': user.LAST_NAME,
                        'is_superuser': user.IS_SUPERUSER,
                        'permissions': user.DESIGNATION.PERMISSIONS
                    }
                }, status=status.HTTP_200_OK)
            
            return Response({
                'status': 'error',
                'message': message
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except CustomUser.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Invalid user'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Token generation error: {str(e)}")
            return Response({
                'status': 'error',
                'message': 'An error occurred during authentication'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RequestPasswordResetView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({
                'status': 'error',
                'message': 'Please provide USER_ID'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(USER_ID=user_id.upper())
            
            if not user.IS_ACTIVE:
                return Response({
                    'status': 'error',
                    'message': 'Account is not active'
                }, status=status.HTTP_403_FORBIDDEN)

            # Generate and send OTP
            otp = user.generate_otp()
            
            try:
                send_mail(
                    subject='Password Reset OTP - College ERP',
                    message=(
                        f'Dear {user.FIRST_NAME},\n\n'
                        f'Your password reset OTP is: {otp}\n'
                        f'This OTP will expire in 3 minutes.\n\n'
                        f'If you did not request a password reset, please ignore this email.\n\n'
                        f'Best regards,\n'
                        f'College ERP Team'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.EMAIL],
                    fail_silently=False,
                )
                
                return Response({
                    'status': 'success',
                    'message': 'Password reset OTP sent successfully',
                    'email': user.EMAIL[:3] + '*' * (len(user.EMAIL.split('@')[0]) - 3) + '@' + user.EMAIL.split('@')[1]
                }, status=status.HTTP_200_OK)
                
            except Exception as e:
                user.OTP_SECRET = None
                user.save()
                return Response({
                    'status': 'error',
                    'message': 'Failed to send OTP email'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except CustomUser.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

class VerifyResetOTPView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        otp = request.data.get('otp')
        
        if not user_id or not otp:
            return Response({
                'status': 'error',
                'message': 'Please provide both USER_ID and OTP'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(USER_ID=user_id.upper())
            is_valid, message = user.verify_otp(otp)
            
            return Response({
                'status': 'success' if is_valid else 'error',
                'message': message,
                'verified': is_valid
            }, status=status.HTTP_200_OK if is_valid else status.HTTP_400_BAD_REQUEST)
            
        except CustomUser.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        
        if not all([user_id, otp, new_password]):
            return Response({
                'status': 'error',
                'message': 'Please provide USER_ID, OTP and new password'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(USER_ID=user_id.upper())
            is_valid, message = user.verify_otp(otp)
            
            if not is_valid:
                return Response({
                    'status': 'error',
                    'message': message
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Set new password
            user.set_password(new_password)
            user.OTP_SECRET = None  # Clear OTP after successful password reset
            user.save()
            
            return Response({
                'status': 'success',
                'message': 'Password reset successful'
            }, status=status.HTTP_200_OK)
            
        except CustomUser.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

class MasterTableListView(APIView):
    def get(self, request):
        master_tables = [
            {"name": "country", "display_name": "Country", "endpoint": "http://localhost:8000/api/master/countries/"},
            {"name": "state", "display_name": "State", "endpoint": "http://localhost:8000/api/master/states/"},
            {"name": "city", "display_name": "City", "endpoint": "http://localhost:8000/api/master/cities/"},
            {"name": "currency", "display_name": "Currency", "endpoint": "http://localhost:8000/api/master/currencies/"},
            {"name": "language", "display_name": "Language", "endpoint": "http://localhost:8000/api/master/languages/"},
            {"name": "university", "display_name": "University", "endpoint": "http://localhost:8000/api/master/universities/"},
            {"name": "institute", "display_name": "Institute", "endpoint": "http://localhost:8000/api/master/institutes/"},
            {"name": "program", "display_name": "Program", "endpoint": "http://localhost:8000/api/master/programs/"},
            {"name": "branch", "display_name": "Branch", "endpoint": "http://localhost:8000/api/master/branches/"},
            {"name": "designation", "display_name": "Designation", "endpoint": "http://localhost:8000/api/master/designations/"},
            {"name": "category", "display_name": "Category", "endpoint": "http://localhost:8000/api/master/categories/"}
        ]
        return Response(master_tables)

class CountryViewSet(viewsets.ModelViewSet):
    queryset = COUNTRY.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Get the current user from the request
        user = self.request.user
        serializer.save(
            CREATED_BY=user.USER_ID,
            UPDATED_BY=user.USER_ID
        )

    def perform_update(self, serializer):
        # Get the current user from the request
        user = self.request.user
        serializer.save(UPDATED_BY=user.USER_ID)
