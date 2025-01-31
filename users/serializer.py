from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import user_logged_in
from rest_framework import serializers
from .models import User
from .validators import lowercase_validator, uppercase_validator, \
    number_validator
from referrals.services import referral_update


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        validators=[lowercase_validator, uppercase_validator, number_validator]
    )

    referral_code = serializers.CharField(write_only=True, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'referral_code']

    def create(self, validated_data):
        referral_code = validated_data['referral_code']
        email = validated_data['email']
        del validated_data['referral_code']
        result = User.objects.create_user(**validated_data)
        referral_update(referral_code=referral_code, email=email)
        return result


class CustomGoogleTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        data = {}
        refresh = RefreshToken.for_user(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    class NoActiveUserException(Exception):
        def __init__(self):
            self.error_code = 'noActiveUser'

    class InvalidCredentialsException(Exception):
        def __init__(self):
            self.error_code = 'invalidCredentials'

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def _get_exception(self, email):
        user = User.objects.filter(email=email)
        return self.NoActiveUserException() if user.filter(is_active=False).exists() else \
            self.InvalidCredentialsException()

    def _validate(self, attrs):
        try:
            return super().validate(attrs)
        except AuthenticationFailed:
            raise self._get_exception(attrs.get('email'))

    def validate(self, attrs):
        request = self.context['request']
        data = self._validate(attrs)
        user_logged_in.send(sender=User, request=request, user=self.user)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        validators=[lowercase_validator, uppercase_validator, number_validator]
    )

    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'repeat_password']

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance

    def validate(self, attrs):
        self.fields_match_validator(
            attrs, 'password', 'repeat_password', 'Las passwords deben coincidir')
        return super().validate(attrs)

    @staticmethod
    def fields_match_validator(data, field_name1, field_name2, error_message=''):
        field1 = data.get(field_name1)
        field2 = data.get(field_name2)
        if field1 != field2:
            raise serializers.ValidationError(error_message)


class ChangePasswordSerializer(serializers.ModelSerializer):
    actual_password = serializers.CharField(write_only=True)

    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        validators=[lowercase_validator, uppercase_validator, number_validator]
    )

    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'repeat_password', 'actual_password']

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance

    def validate(self, attrs):
        self.fields_match_validator(
            attrs, 'password', 'repeat_password', 'Las passwords deben coincidir')
        return super().validate(attrs)

    @staticmethod
    def fields_match_validator(data, field_name1, field_name2, error_message=''):
        field1 = data.get(field_name1)
        field2 = data.get(field_name2)
        if field1 != field2:
            raise serializers.ValidationError(error_message)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'is_superuser', 'referral_id']

    def create():
        pass

    def update():
        pass


class ResendEmailValidation(serializers.Serializer):
    uidb64 = serializers.CharField(max_length=255, required=False)
    email = serializers.CharField(max_length=255, required=False)

    def validate(self, attrs):
        self.fields_mutually_exclusive(attrs)
        self.empty_fields(attrs)
        return super().validate(attrs)

    @staticmethod
    def fields_mutually_exclusive(data):
        field1 = data.get('uidb64', None)
        field2 = data.get('email', None)
        if field1 is not None and field2 is not None:
            raise serializers.ValidationError('Los campos son mutuamente exclusivos')

    @staticmethod
    def empty_fields(data):
        field1 = data.get('uidb64', None)
        field2 = data.get('email', None)
        if field1 is None and field2 is None:
            raise serializers.ValidationError('Debe existir al menos uno de los campos requeridos: email, uidb64')
