import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Profile
from .serializers import ProfileSerializer
from users.test_utils import get_credentials
from users.models import User

profile_test_data = {
    'first_name': '',
    'last_name': '',
    'nro_dni': '',
    'cellphone': '',
    'condicion_iva': '',
    'tipo_factura': '',
    'cuit': '',
    'direccion': ''
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
            reverse('profiles:retrieve-update-user-profile'),
            {'user_id': self.user.id},
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_call_invalid(self):
        """ Profile does not exists """
        self.user.profile.delete()
        self.user.save()
        response = self.client.get(
            reverse('profiles:retrieve-update-user-profile'),
            {'user_id': self.user.id},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'profiles.retrieve.doesNotExists')

    def test_update_call(self):
        payload = json.dumps(profile_test_data)
        response = self.client.put(
            reverse('profiles:retrieve-update-user-profile'),
            QUERY_STRING=f'user_id={self.user.id}',
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
            reverse('profiles:retrieve-update-user-profile'),
            QUERY_STRING=f'user_id={self.user.id}',
            data=payload,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'profiles.update.doesNotExists')

    def test_update_call_invalid_2(self):
        """ Invalid data """
        payload = json.dumps({'invalid': 'data'})
        response = self.client.put(
            reverse('profiles:retrieve-update-user-profile'),
            QUERY_STRING=f'user_id={self.user.id}',
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error_code'],
                         'profiles.update.invalidData')


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
                               'tipo_factura', 'cuit', 'direccion', ])

    def test_email_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['email'], self.user.email)

    def test_valid_data_serializer(self):
        serializer = ProfileSerializer(data=profile_test_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_serializer(self):
        serializer = ProfileSerializer(data={'asdf': 'asdf'})
        self.assertFalse(serializer.is_valid())
