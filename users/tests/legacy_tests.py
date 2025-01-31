import json
import pytest
from users.models import User
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status
from django.test import TestCase, tag
from users.tokens import email_validation_token
from django.utils.http import urlsafe_base64_encode
from users.test_utils import get_credentials, create_user
from rest_framework.serializers import ValidationError
from users.emails import EmailValidation, ResetPasswordEmail
from django.utils.encoding import force_str, force_bytes
from users.validators import number_validator, uppercase_validator, lowercase_validator
from users.serializer import RegistrationSerializer, ResetPasswordSerializer, ChangePasswordSerializer


class UserTestCase(TestCase):

    def setUp(self):
        User.objects.create(email='test@test.com', password='asdfF3')

    def test_string_representation(self):
        user = User.objects.get(email='test@test.com')
        self.assertEqual(str(user), user.email)

    def test_username_field_is_email(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')


class EmailValidationTokenAPIViewTestCase(TestCase):

    def setUp(self):
        user = User(email="test13@test.com", password="test")
        user.save()
        self.token = email_validation_token.make_token(user)
        self.uidb64 = force_str(urlsafe_base64_encode(force_bytes(user.pk)))

    def test_email_validation_valid(self):
        payload = json.dumps({
            'uidb64': self.uidb64,
            'token': self.token
        })
        response = self.client.post(
            reverse('users:email-validation'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_validation_invalid(self):
        payload = json.dumps({
            'uidb64': self.uidb64,
            'token': f'{self.token}-ups'
        })
        response = self.client.post(
            reverse('users:email-validation'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'users.emailValidation.invalid')


@tag('user_registration_serializer')
class RegistrationSerializerTestCase(TestCase):

    def setUp(self):
        self.user_attributes = {
            'email': 'test6@test.com', 'password': 'asdfF5'}
        self.serializer_data = {
            'email': 'test7@test.com',
            'password': 'asdfF5',
            'referral_code': None
        }

        self.user = User.objects.create(**self.user_attributes)
        self.serializer = RegistrationSerializer(instance=self.user)

    def test_containt_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['email'])

    def test_email_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['email'], self.user_attributes['email'])

    def test_valid_data_serializer(self):
        serializer = RegistrationSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_serializer(self):
        serializer = RegistrationSerializer(data=self.user_attributes)
        self.assertFalse(serializer.is_valid())

    def test_invalid_data_exception(self):
        serializer = RegistrationSerializer(data=self.user_attributes)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_create_serializer(self):
        serializer = RegistrationSerializer(data=self.serializer_data)
        serializer.is_valid()
        self.assertEqual(str(serializer.create(
            serializer.validated_data)), self.serializer_data['email'])


class PasswordValidatorsTestCase(TestCase):
    valid_pass = 'asdfF5'
    invalid_lower_pass = 'ASDFF5'
    invalid_upper_pass = 'asdff5'
    invalid_number_pass = 'asdfFF'

    def test_valid_lowercase_validator(self):
        self.assertEqual(lowercase_validator(self.valid_pass), self.valid_pass)

    def test_valid_uppercase_validator(self):
        self.assertEqual(uppercase_validator(self.valid_pass), self.valid_pass)

    def test_valid_number_validator(self):
        self.assertEqual(number_validator(self.valid_pass), self.valid_pass)

    def test_invalid_lowercase_validator(self):
        with self.assertRaises(ValidationError):
            lowercase_validator(self.invalid_lower_pass)

    def test_invalid_uppercase_validator(self):
        with self.assertRaises(ValidationError):
            uppercase_validator(self.invalid_upper_pass)

    def test_invalid_number_validator(self):
        with self.assertRaises(ValidationError):
            number_validator(self.invalid_number_pass)


class LoginUrlTestCase(TestCase):

    def setUp(self):
        self.password = 'testT5'
        self.activeUser = User.objects.create_user(
            email='test13@test.com', password=self.password)
        self.inactiveUser = User.objects.create_user(
            email='test21@test.com', password=self.password)
        self.activeUser.is_active = True
        self.activeUser.save()
        self.inactiveUser.save()

    def test_success_login(self):
        payload = json.dumps({
            'email': self.activeUser.email,
            'password': self.password
        })
        response = self.client.post(
            reverse('users:user-login'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_login_user_inactive(self):
        payload = json.dumps({
            'email': self.inactiveUser.email,
            'password': self.password
        })
        response = self.client.post(
            reverse('users:user-login'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['error_code'], 'users.login.noActiveUser')

    def test_fail_login_user_invalid_email(self):
        payload = json.dumps({
            'email': 'testinvalid@test.invalid',
            'password': self.password
        })
        response = self.client.post(
            reverse('users:user-login'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['error_code'], 'users.login.invalidCredentials')

    def test_fail_login_user_invalid_password(self):
        payload = json.dumps({
            'email': self.activeUser.email,
            'password': 'someinvalid'
        })
        response = self.client.post(
            reverse('users:user-login'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['error_code'],
                         'users.login.invalidCredentials')


class EmailValidationTestCase(TestCase):

    def setUp(self):
        self.user = User(email="test13@test.com", password="test")
        self.user.save()

    def test_get_validation_message_ok(self):
        data = EmailValidation._generate_validation_data(self.user)
        self.assertIs(type(data), dict)
        self.assertTrue('uid' in data)
        self.assertTrue('email' in data)
        self.assertTrue('token' in data)
        self.assertTrue('domain' in data)


@tag('reset_password_email')
class ResetPasswordEmailTestCase(TestCase):

    def setUp(self):
        self.user = User(email="test13@test.com", password="test")
        self.user.save()

    def test_get_validation_message_ok(self):
        message = ResetPasswordEmail.get_validation_message(self.user)
        self.assertIs(type(message), dict)
        self.assertTrue('uid' in message)
        self.assertTrue('email' in message)
        self.assertTrue('token' in message)
        self.assertTrue('domain' in message)

    def test_get_validation_message_error(self):
        with self.assertRaises(AttributeError):
            ResetPasswordEmail.get_validation_message('')


@tag('send_reset_password_email')
class SendResetPasswordEmailAPIViewTestCase(TestCase):
    def setUp(self):
        self.userData = {
            "email": "test13@test.com",
            "password": "testT6"
        }
        user = User(**self.userData)
        user.save()

    @patch('requests.post')
    def test_send_reset_password_email_valid(self, mock_post):
        mock_post.return_value.json.return_value = {}
        mock_post.return_value.status_code = status.HTTP_200_OK
        payload = json.dumps({
            'email': self.userData.get('email')
        })
        response = self.client.post(
            reverse('users:send-reset-password-email'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_send_reset_password_email_invalid_email(self):
        payload = json.dumps({
            'email': 'xxxxx'
        })
        response = self.client.post(
            reverse('users:send-reset-password-email'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'users.sendResetPasswordEmail.user')

    def test_send_reset_password_not_register_email(self):
        payload = json.dumps({
            'email': 'a___@___a.com'
        })
        response = self.client.post(
            reverse('users:send-reset-password-email'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'users.sendResetPasswordEmail.user')


@tag('reset_password')
class ResetPasswordAPIViewTestCase(TestCase):

    def setUp(self):
        user = User(email="test13@test.com", password="test")
        user.save()
        self.token = email_validation_token.make_token(user)
        self.uidb64 = force_str(urlsafe_base64_encode(force_bytes(user.pk)))

    def test_reset_password_valid(self):
        payload = json.dumps({
            'uidb64': self.uidb64,
            'token': self.token,
            'password': 'test2T',
            'repeat_password': 'test2T',
        })
        response = self.client.post(
            reverse('users:reset-password'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_invalid(self):
        payload = json.dumps({
            'uidb64': self.uidb64,
            'token': f'{self.token}-ups',
            'password': 'asdf',
            'repeat_password': 'asdf'
        })
        response = self.client.post(
            reverse('users:reset-password'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'users.resetPassword.invalid')


@tag('reset_password_serializer')
class ResetPasswordSerializerTestCase(TestCase):

    def setUp(self):
        self.user_attributes = {
            'email': 'test13@test.com', 'password': 'asdfF5'}
        self.new_password = 'asdfF6'
        self.user = User(
            email=self.user_attributes.get('email'),
            password=self.user_attributes.get('password')
        )
        self.user.save()
        self.serializer_data = {
            'token': force_str(urlsafe_base64_encode(force_bytes(self.user.pk))),
            'uidb64': email_validation_token.make_token(self.user),
            'password': self.new_password,
            'repeat_password': self.new_password
        }

    def test_valid_data_serializer(self):
        serializer = ResetPasswordSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_serializer(self):
        serializer = ResetPasswordSerializer(data=self.user_attributes)
        self.assertFalse(serializer.is_valid())

    def test_invalid_data_exception(self):
        serializer = ResetPasswordSerializer(data=self.user_attributes)
        with self.assertRaises(ValidationError):
            serializer.validate(attrs=self.user_attributes)

    def test_serializer_update(self):
        serializer = ResetPasswordSerializer(data=self.serializer_data)
        serializer.is_valid()
        self.assertEqual(
            str(serializer.update(self.user, serializer.validated_data)),
            self.user_attributes.get('email')
        )


@tag('change_password')
class ChangePasswordAPIViewTestCase(TestCase):

    def setUp(self):
        self.user_data = {
            'email': 'test@test.com',
            'password': 'test1T'
        }
        self.user = create_user(**self.user_data, is_superuser=False)
        self.credentials = get_credentials(
            self.client,
            **self.user_data,
            new_user=False
        )

    def test_change_password_valid(self):
        payload = json.dumps({
            'actual_password': self.user_data['password'],
            'password': 'test2T',
            'repeat_password': 'test2T',
        })
        response = self.client.post(
            reverse('users:change-password', kwargs={'pk': self.user.pk}),
            data=payload,
            content_type='application/json',
            **self.credentials
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_invalid(self):
        payload = json.dumps({
            'actual_password': 'test1T',
            'password': 'asdf',
            'repeat_password': 'asdf'
        })
        response = self.client.post(
            reverse('users:change-password', kwargs={'pk': self.user.pk}),
            data=payload,
            content_type='application/json',
            **self.credentials
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'users.changePassword.invalid')


@tag('change_password_serializer')
class ChangePasswordSerializerTestCase(TestCase):

    def setUp(self):
        self.user_attributes = {
            'email': 'test13@test.com', 'password': 'asdfF5'}
        self.new_password = 'asdfF6'
        self.user = User(
            email=self.user_attributes.get('email'),
            password=self.user_attributes.get('password')
        )
        self.user.save()
        self.serializer_data = {
            'actual_password': 'asdfF5',
            'password': self.new_password,
            'repeat_password': self.new_password
        }

    def test_valid_data_serializer(self):
        serializer = ChangePasswordSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_serializer(self):
        serializer = ChangePasswordSerializer(data=self.user_attributes)
        self.assertFalse(serializer.is_valid())

    def test_invalid_data_exception(self):
        serializer = ChangePasswordSerializer(data=self.user_attributes)
        with self.assertRaises(ValidationError):
            serializer.validate(attrs=self.user_attributes)

    def test_serializer_update(self):
        serializer = ChangePasswordSerializer(data=self.serializer_data)
        serializer.is_valid()
        self.assertEqual(
            str(serializer.update(self.user, serializer.validated_data)),
            self.user_attributes.get('email')
        )


class IsSuperUserAPIViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('users:is-superuser')

    def test_is_superuser_unauth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_is_superuser_true(self):
        self.credentials = get_credentials(
            self.client,
            email="test_super_user@gmail.com",
            password="test",
            new_user=True,
            is_superuser=True
        )
        response = self.client.get(self.url, **self.credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

    def test_is_superuser_false(self):
        self.credentials = get_credentials(
            self.client,
            email="test_user@gmail.com",
            password="test",
            new_user=True,
            is_superuser=False
        )
        response = self.client.get(self.url, **self.credentials)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json())


class GetUserAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com', is_active=True)

    def test_get_user(self):
        response = self.client.get(
            reverse('users:get-user', kwargs={'pk': self.user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id' in response.json())

    def test_get_user_does_not_exist(self):
        response = self.client.get(
            reverse('users:get-user', kwargs={'pk': self.user.pk + 1})
        )
        self.assertEqual(response.status_code, 404)


@pytest.mark.parametrize(
    'email, expected_status_code, expected_body',
    [
        ('exists@test.com', status.HTTP_200_OK, {
            'email': 'exists@test.com',
            'is_active': False,
            'is_superuser': False,
            'referral_id': ''
        }),
        ('noexists@test.com', status.HTTP_404_NOT_FOUND, {}),
    ])
@pytest.mark.django_db
def test_by_email_api_view(client, email, expected_status_code, expected_body):
    User.objects.create_user('exists@test.com', 'TestPass1234')
    endpoint = reverse('users:by-email', kwargs={'email': email})
    response = client.get(endpoint)
    response.json().pop('id', None)
    assert response.status_code == expected_status_code
    assert response.json() == expected_body


@pytest.mark.django_db
@pytest.mark.parametrize('refresh_token, expected_status, expected_response', [
    [None, status.HTTP_200_OK, {"access": "", "refresh": ""}],
    ['test_refresh_invalido', status.HTTP_401_UNAUTHORIZED,
     {"detail": "Token is invalid or expired", "code": "token_not_valid"}]
])
def test_refresh_token(client, refresh_token, expected_status, expected_response):
    create_user("franco@xcapit.com", "Hola12345", False)

    payload_access = json.dumps({
        'email': 'franco@xcapit.com',
        'password': 'Hola12345'
    })

    credentials = client.post(
        reverse('users:user-login'), data=payload_access,
        content_type='application/json').data

    refresh_token_post = refresh_token if refresh_token is not None else credentials.get("refresh")

    payload_refresh = json.dumps({
        'refresh': refresh_token_post
    })

    response = client.post(
        reverse('users:refresh_token'), data=payload_refresh,
        content_type='application/json')

    assert response.status_code == expected_status

    for key, value in expected_response.items():
        assert key in response.data
        if len(value) > 0:
            assert value in response.data[key]
