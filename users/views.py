from .serializer import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .serializer import RegistrationSerializer, ResetPasswordSerializer, \
    ChangePasswordSerializer
from .models import User
from .tokens import email_validation_token
from .emails import EmailValidation, ResetPasswordEmail
from core.helpers import ResponseHelper
from rest_framework.exceptions import AuthenticationFailed
from .services import get_hashid
from rest_framework.permissions import IsAuthenticated
from users.serializer import UserSerializer
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
add_error_code = ResponseHelper.add_error_code


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            response = Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'users.registration.invalidData')
        user_instance = serializer.save()
        user_instance.referral_id = get_hashid(user_instance.pk)
        user_instance.save()
        EmailValidation.send(user_instance)
        return Response({}, status=status.HTTP_201_CREATED)


class EmailValidationTokenAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            uid = force_text(urlsafe_base64_decode(
                request.data.get('uidb64', '')))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and email_validation_token.check_token(
                user, request.data.get('token', '')):
            user.is_active = True
            user.save()
            return Response({'isValid': True}, status.HTTP_200_OK)
        else:
            response = Response({'isValid': False},
                                status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'users.emailValidation.invalid')


class SendEmailValidationTokenAPIView(APIView):

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            uid = force_text(urlsafe_base64_decode(
                request.data.get('uidb64', '')))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None:
            EmailValidation.send(user)
            return Response({}, status.HTTP_200_OK)
        else:
            response = Response({}, status.HTTP_400_BAD_REQUEST)
            return add_error_code(response,
                                  'users.sendEmailValidationToken.user')


class ObtainJWTView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    # Enviar error code cuando no puede loguear
    def post(self, request, *args, **kwargs):
        try:
            return super(ObtainJWTView, self).post(request, *args, **kwargs)
        except AuthenticationFailed as e:
            return add_error_code(Response(
                {'error': e.get_full_details()},
                status=status.HTTP_401_UNAUTHORIZED),
                'users.login.invalidCredentials')


class SendResetPasswordEmailAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            user = User.objects.get(email=request.data.get('email', ''))
        except(TypeError, ValueError, User.DoesNotExist):
            user = None
        if user is not None:
            ResetPasswordEmail.send(user)
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
            uid = force_text(urlsafe_base64_decode(
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

    def post(self, request):
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
