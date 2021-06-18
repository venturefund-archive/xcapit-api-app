from core.clients import NotificationsClient
from .serializer import CustomTokenObtainPairSerializer, ResendEmailValidation, \
    CustomGoogleTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .serializer import RegistrationSerializer, ResetPasswordSerializer, \
    ChangePasswordSerializer
from .models import User
from .tokens import email_validation_token
from .emails import EmailValidation, ResetPasswordEmail
from core.helpers import ResponseHelper
from rest_framework.exceptions import AuthenticationFailed
from .services import get_hashid, ResendEmailValidationService
from rest_framework.permissions import IsAuthenticated
from users.serializer import UserSerializer
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from referrals.services import validate_referral
from referrals.models import Referral
from google.oauth2 import id_token as token_auth
from google.auth.transport import requests as google_auth_request
from datetime import datetime
from django.conf import settings


add_error_code = ResponseHelper.add_error_code


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        user['referral_code'] = user.get('referral_code')
        if user['referral_code'] and not User.objects.filter(
                referral_id=user['referral_code']
        ).exists():
            response = Response({}, status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'users.registration.referralIdNotExists')
        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            response = Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'users.registration.invalidData')
        user_instance = serializer.save()
        user_instance.referral_id = get_hashid(user_instance.pk)
        user_instance.save()
        email_validation = EmailValidation()
        email_validation.send(user_instance)
        user_serializer = UserSerializer(instance=user_instance)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


class ByEmailAPIView(APIView):
    serializer_class = UserSerializer

    def get(self, request, email):
        """ Get user by email

        Parameters
        ----------
        email: str
            User email

        Returns
        -------

        """
        users = User.objects.filter(email=email)
        if not users.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        user = users.first()
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmailValidationTokenAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            uid = force_str(urlsafe_base64_decode(
                request.data.get('uidb64', '')))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and email_validation_token.check_token(
                user, request.data.get('token', '')):
            user.is_active = True
            user.save()
            referral_queryset = Referral.objects.filter(email=user.email)
            if referral_queryset.exists():
                referral = referral_queryset.first()
                validate_referral(referral.referral_id, referral.email)
            return Response({'isValid': True}, status.HTTP_200_OK)
        else:
            response = Response({'isValid': False},
                                status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'users.emailValidation.invalid')


class SendEmailValidationTokenAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = ResendEmailValidation

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            resend_email_service = ResendEmailValidationService(request.data)
            response = resend_email_service.execute()
        else:
            response = Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        return response


class LoginWithGoogleAPIView(APIView):
    serializer_class = CustomGoogleTokenObtainPairSerializer

    def post(self, request):
        id_token = request.data['id_token']
        idinfo = self.verify_google_oauth2(id_token)

        if idinfo['aud'] not in [settings.CLIENT_ID_1, settings.CLIENT_ID_2, settings.CLIENT_ID_3]:
            response = Response({'error': 'Error client access'}, status=status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'users.login.notClientAccess')

        if idinfo['email_verified'] is not True:
            response = Response({'error': 'Google account not verified'}, status=status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'users.login.notVerifiedGoogleAccount')

        user_queryset = User.objects.filter(email=idinfo['email'])

        if not user_queryset.exists():
            user = self.register_user(idinfo)
        else:
            user = user_queryset.first()
            if len(user.password) > 0:
                response = Response({'error': 'User register with another account'}, status=status.HTTP_400_BAD_REQUEST)
                return add_error_code(response, 'users.login.notGoogleLoginUser')

        data = self.serializer_class.get_token(user)

        self.update_last_login(user)

        return Response(data, status.HTTP_200_OK)

    @staticmethod
    def verify_google_oauth2(id_token):
        req = google_auth_request.Request()

        return token_auth.verify_oauth2_token(id_token, req)

    @staticmethod
    def register_user(info):
        user_instance = User.objects.create(email=info['email'])
        user_instance.is_active = True
        user_instance.referral_id = get_hashid(user_instance.pk)
        user_instance.last_login = datetime.utcnow()
        user_instance.save()

        return user_instance

    @staticmethod
    def update_last_login(user_instance):
        user_instance.last_login = datetime.utcnow()
        user_instance.save()

        return user_instance


class ObtainJWTView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    _error_code_prefix = 'users.login.'

    def __init__(self, *args, **kwargs):
        super(ObtainJWTView, self).__init__(*args, **kwargs)
        self._response = Response({}, status=status.HTTP_200_OK)

    def _set_response_status(self, status_code: int):
        self._response.status_code = status_code

    def _add_error_code(self, error_code: str):
        self._response = add_error_code(self._response, f'{self._error_code_prefix}{error_code}')

    def post(self, request, *args, **kwargs):
        if len(request.data['password']) == 0:
            self._set_response_status(status.HTTP_401_UNAUTHORIZED)
            self._add_error_code(self.serializer_class.InvalidCredentialsException().error_code)

        try:
            self._response = super(ObtainJWTView, self).post(request, *args, **kwargs)
        except (
                self.serializer_class.InvalidCredentialsException,
                self.serializer_class.NoActiveUserException
        ) as e:
            self._set_response_status(status.HTTP_401_UNAUTHORIZED)
            self._add_error_code(e.error_code)
        finally:
            return self._response


class SendResetPasswordEmailAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            user = User.objects.get(email=request.data.get('email', ''))
        except(TypeError, ValueError, User.DoesNotExist):
            user = None
        if user is not None:
            reset_email = ResetPasswordEmail()
            response = reset_email.send(user)

            if response.status_code != status.HTTP_200_OK:
                response = Response({'error': 'Email not sent'}, status=status.HTTP_400_BAD_REQUEST)
                return add_error_code(response, 'referrals.create.emailDidNotSend')

            return Response({}, status.HTTP_200_OK)
        else:
            response = Response({}, status.HTTP_400_BAD_REQUEST)
            return add_error_code(
                response,
                'users.sendResetPasswordEmail.user'
            )


class ResetPasswordAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        try:
            uid = force_str(urlsafe_base64_decode(
                request.data.get('uidb64', '')))
            user = User.objects.get(pk=uid)
            serializer = self.serializer_class(data=request.data)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and email_validation_token.check_token(
                user, request.data.get('token', '')) and serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response({}, status.HTTP_200_OK)
        else:
            response = Response({}, status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'users.resetPassword.invalid')


class ChangePasswordAPIView(APIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request, pk):
        try:
            request.user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({}, status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid() or not request.user.check_password(
                request.data.get('actual_password')):
            response = Response({}, status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'users.changePassword.invalid')
        serializer.update(request.user, serializer.validated_data)
        return Response({}, status.HTTP_200_OK)


class IsSuperUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(request.user.is_superuser, status=status.HTTP_200_OK)


class GetUserAPIView(APIView):
    serializer_class = UserSerializer

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({}, status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(user)
        profile = Profile.objects.filter(user=user)
        user = serializer.data
        user['profile'] = None
        if len(profile):
            profile_serializer = ProfileSerializer(profile[0])
            user['profile'] = profile_serializer.data
        return Response(user, status=status.HTTP_200_OK)
