import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Profile
from .serializers import ProfileSerializer
from users.test_utils import get_credentials
from users.models import User

personal_data = {
    'nro_dni': '',
    'cellphone': '',
    'cuit': '',
    'direccion': '',
}

fiscal_data = {
    'condicion_iva': '',
    'tipo_factura': '',
    'cuit': '',
    'pais': ''
}

profile_test_data = {
    'first_name': '',
    'last_name': '',
    'nro_dni': '',
    'cellphone': '',
    'condicion_iva': '',
    'tipo_factura': '',
    'cuit': '',
    'direccion': '',
    'pais': ''
}

user_test_data = {
    'email': 'test@test.com',
    'password': 'asdfF3'
}


class ProfileTestCase(TestCase):

    def setUp(self):
        self.user = User(email=user_test_data.get('email'), is_active=True)
        self.user.set_password(user_test_data.get('password'))
        self.user.save()
        self.profile = Profile.objects.get(user=self.user)

    def test_string_representation(self):
        self.assertEqual(str(self.profile), user_test_data.get('email'))


class ProfileRetrieveUpdateAPIViewTestCase(TestCase):
    def setUp(self):
        self.credentials = get_credentials(
            self.client,
            email="test13@test.com",
            password="test1T"
        )
        self.user = User.objects.get(email='test13@test.com')

    def test_retrieve_call(self):
        response = self.client.get(
            reverse('profiles:retrieve-update-user-profile',
                    kwargs={'user_id': self.user.id}),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_call_invalid(self):
        """ Profile does not exists """
        self.user.profile.delete()
        self.user.save()
        response = self.client.get(
            reverse('profiles:retrieve-update-user-profile',
                    kwargs={'user_id': self.user.id}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'profiles.retrieve.doesNotExists')

    def test_update_call(self):
        payload = json.dumps(profile_test_data)
        response = self.client.put(
            reverse('profiles:retrieve-update-user-profile',
                    kwargs={'user_id': self.user.id}),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_call_invalid_1(self):
        """ Profile does not exists """
        self.user.profile.delete()
        self.user.save()
        payload = json.dumps(profile_test_data)
        response = self.client.put(
            reverse('profiles:retrieve-update-user-profile',
                    kwargs={'user_id': self.user.id}),
            data=payload,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'profiles.update.doesNotExists')

    def test_update_personal_data(self):
        """ Invalid data """
        payload = json.dumps(personal_data)
        response = self.client.put(
            reverse('profiles:retrieve-update-user-profile',
                    kwargs={'user_id': self.user.id}),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_fiscal_data(self):
        """ Invalid data """
        payload = json.dumps(fiscal_data)
        response = self.client.put(
            reverse('profiles:retrieve-update-user-profile',
                    kwargs={'user_id': self.user.id}),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileSerializerTestCase(TestCase):

    def setUp(self):
        self.profile_attributes = profile_test_data
        self.serializer_data = profile_test_data
        self.serializer_data['email'] = user_test_data.get('email')
        self.user = User.objects.create(**user_test_data)
        self.profile = Profile.objects.get(user=self.user)
        self.serializer = ProfileSerializer(instance=self.profile)

    def test_containt_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(),
                              ['email', 'first_name', 'last_name',
                               'nro_dni', 'cellphone', 'condicion_iva',
                               'tipo_factura', 'cuit', 'direccion', 'pais'])

    def test_email_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['email'], self.user.email)

    def test_valid_data_serializer(self):
        serializer = ProfileSerializer(data=profile_test_data)
        self.assertTrue(serializer.is_valid())

    def test_valid_personal_data_serializer(self):
        serializer = ProfileSerializer(data=personal_data)
        self.assertTrue(serializer.is_valid())

    def test_valid_fiscal_data_serializer(self):
        serializer = ProfileSerializer(data=fiscal_data)
        self.assertTrue(serializer.is_valid())

    def test_valid_name_keys_data_serializer(self):
        serializer = ProfileSerializer(
            data={'first_name': 'Test', 'last_name': 'Test'})
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_serializer(self):
        serializer = ProfileSerializer(data={'asdas': 'asdas'})
        self.assertFalse(serializer.is_valid())

    def test_personal_invalid_data_serializer(self):
        personal_data_invalid = personal_data.copy()
        personal_data_invalid.pop('cellphone')
        serializer = ProfileSerializer(data=personal_data_invalid)
        self.assertFalse(serializer.is_valid())

    def test_fiscal_invalid_data_serializer(self):
        fiscal_data_invalid = fiscal_data.copy()
        fiscal_data_invalid.pop('cuit')
        serializer = ProfileSerializer(data=fiscal_data_invalid)
        self.assertFalse(serializer.is_valid())

    def test_invalid_name_keys_data_serializer(self):
        serializer = ProfileSerializer(
            data={'last_name': 'Test'})
        self.assertFalse(serializer.is_valid())

