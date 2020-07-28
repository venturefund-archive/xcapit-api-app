import json
from unittest.mock import patch

from django.test import TestCase, tag
from rest_framework import status
from rest_framework.serializers import ValidationError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.urls import reverse
from django.utils.safestring import SafeText

from .models import User
from .serializer import RegistrationSerializer, ResetPasswordSerializer, \
    ChangePasswordSerializer
from .validators import number_validator, uppercase_validator, \
    lowercase_validator
from .tokens import email_validation_token
from .emails import EmailValidation, ResetPasswordEmail
from .test_utils import get_credentials, create_user


class UserTestCase(TestCase):

    def setUp(self):
        User.objects.create(email='test@test.com', password='asdfF3')

    def test_string_representation(self):
        user = User.objects.get(email='test@test.com')
        self.assertEqual(str(user), user.email)

    def test_username_field_is_email(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')


@tag('user_registration')
class RegistrationAPIViewTestCase(TestCase):
    @patch('requests.post')
    def test_user_registration_valid(self, mock_post):
        mock_post.return_value.json.return_value = {}
        mock_post.return_value.status_code = status.HTTP_200_OK
        payload = json.dumps({
            'email': 'test6@test.com',
            'repeat_email': 'test6@test.com',
            'password': 'asdfF5',
            'repeat_password': 'asdfF5',
            'referral_code': None
        })
        response = self.client.post(
            reverse('users:user-registration'), data=payload,
            content_type='application/json')
        user = User.objects.get(email='test6@test.com')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(user.referral_id)

    def test_user_registration_invalid_number_pass(self):
        payload = json.dumps({'email': 'test6@test.com',
                              'repeat_email': 'test6@test.com',
                              'password': 'asdfFF',
                              'repeat_password': 'asdfFF'})
        response = self.client.post(
            reverse('users:user-registration'), data=payload,
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'users.registration.invalidData')

    def test_user_registration_invalid_upper_pass(self):
        payload = json.dumps({'email': 'test6@test.com',
                              'repeat_email': 'test6@test.com',
                              'password': 'asdf55',
                              'repeat_password': 'asdf55'})
        response = self.client.post(
            reverse('users:user-registration'), data=payload,
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'users.registration.invalidData')

    def test_user_registration_invalid_lower_pass(self):
        payload = json.dumps({'email': 'test6@test.com',
                              'repeat_email': 'test6@test.com',
                              'password': '1234F1',
                              'repeat_password': '1234F1'})
        response = self.client.post(
            reverse('users:user-registration'), data=payload,
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'users.registration.invalidData')

    def test_user_registration_invalid_min_pass(self):
        payload = json.dumps({'email': 'test6@test.com',
                              'repeat_email': 'test6@test.com',
                              'password': 'asdf',
                              'repeat_password': 'asdf'})
        response = self.client.post(
            reverse('users:user-registration'), data=payload,
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'users.registration.invalidData')

    def test_user_registration_invalid_repeat_pass(self):
        payload = json.dumps({'email': 'test6@test.com',
                              'repeat_email': 'test6@test.com',
                              'password': 'asdfF5',
                              'repeat_password': 'asdfF6'})
        response = self.client.post(
            reverse('users:user-registration'), data=payload,
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'users.registration.invalidData')

    def test_user_registration_invalid_repeat_email(self):
        payload = json.dumps({'email': 'test6@test.com',
                              'repeat_email': 'test5@test.com',
                              'password': 'asdfF6',
                              'repeat_password': 'asdfF6'})
        response = self.client.post(
            reverse('users:user-registration'), data=payload,
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'users.registration.invalidData')

    @patch('requests.post')
    def test_referral_user_registration_valid(self, mock_post):
        mock_post.return_value.json.return_value = {}
        mock_post.return_value.status_code = status.HTTP_200_OK
        referral_user = {
            'email': 'test7@test.com',
            'repeat_email': 'test7@test.com',
            'password': 'asdfF5',
            'repeat_password': 'asdfF5',
            'referral_code': None
        }
        user = create_user(
            email='active@user.com',
            password='power5R',
            is_superuser=False
        )
        user.referral_id = 'ref123'
        user.save()
        credentials = get_credentials(
            self.client,
            email='active@user.com',
            password='power5R',
            new_user=False
        )
        new_referral_response = self.client.post(
            reverse('referrals:referrals',
                    kwargs={'user_id': user.id}),
            data={'email': referral_user.get('email'), 'accepted': True},
            **credentials
        )
        referral_user['referral_code'] = user.referral_id
        response = self.client.post(
            reverse('users:user-registration'), data=json.dumps(referral_user),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        referrals_response = self.client.get(
            reverse('referrals:referrals',
                    kwargs={'user_id': user.id}),
            data={'cursor': '',
                  'ordering': '-accepted,email,created_at'},
            **credentials
        )
        referral = referrals_response.data['results'][0]
        self.assertEqual(referral['email'], referral_user['email'])
        self.assertEqual(referral['email'],
                         new_referral_response.data['email'])
        self.assertTrue(referral['accepted'])
        self.assertEqual(referral['referral_id'], user.referral_id)
        self.assertEqual(
            referral['referral_id'],
            new_referral_response.data['referral_id']
        )

    def test_referral_user_registration_with_invalid_referral_code(self):
        referral_users = [{
            'email': 'test8@test.com',
            'repeat_email': 'test8@test.com',
            'password': 'asdfF5',
            'repeat_password': 'asdfF5',
            'referral_code': 'bad_code'
        }, {
            'email': 'test9@test.com',
            'repeat_email': 'test9@test.com',
            'password': 'asdfF5',
            'repeat_password': 'asdfF5',
            'referral_code': 'MQ'
        }]
        response = self.client.post(
            reverse('users:user-registration'),
            data=json.dumps(referral_users[0]),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'users.registration.referralIdNotExists')
        response = self.client.post(
            reverse('users:user-registration'),
            data=json.dumps(referral_users[1]),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'users.registration.referralIdNotExists')


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


@tag('send_email_validation')
class SendEmailValidationTokenAPIViewTestCase(TestCase):

    def setUp(self):
        user = User(email="test13@test.com", password="test")
        user.save()
        self.token = email_validation_token.make_token(user)
        self.uidb64 = force_str(urlsafe_base64_encode(force_bytes(user.pk)))

    @patch('requests.post')
    def test_send_email_validation_valid(self, mock_post):
        mock_post.return_value.json.return_value = {}
        mock_post.return_value.status_code = status.HTTP_200_OK
        payload = json.dumps({
            'uidb64': self.uidb64
        })
        response = self.client.post(
            reverse('users:send-email-validation'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_send_email_validation_invalid(self):
        payload = json.dumps({
            'uidb64': 'xx'
        })
        response = self.client.post(
            reverse('users:send-email-validation'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'], 'users.sendEmailValidationToken.user')


@tag('user_registration_serializer')
class RegistrationSerializerTestCase(TestCase):

    def setUp(self):
        self.user_attributes = {
            'email': 'test6@test.com', 'password': 'asdfF5'}
        self.serializer_data = {
            'email': 'test7@test.com',
            'repeat_email': 'test7@test.com',
            'password': 'asdfF5',
            'repeat_password': 'asdfF5',
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
            serializer.validate(data=self.user_attributes)

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
        self.assertEqual(response.json()['error_code'],
                         'users.login.invalidCredentials')

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
        self.assertEqual(response.json()['error_code'],
                         'users.login.invalidCredentials')

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
        self.assertIs(type(message), SafeText)
        self.assertGreater(len(message), 0)

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

    def test_send_reset_password_email_valid(self):
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
            'eamil': 'xxxxx'
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
            'eamil': 'a___@___a.com'
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
