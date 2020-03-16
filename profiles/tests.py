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
    'first_name': '',
    'last_name': '',
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
            data=personal_data)
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


class ProfileValidAPIViewTestCase(TestCase):
    def setUp(self):
        self.invalid_profile = profile_test_data.copy()
        if 'email' in self.invalid_profile:
            self.invalid_profile.pop('email')
        self.valid_profile = {
            'first_name': 'Test First',
            'last_name': 'Test Last',
            'nro_dni': '321332155',
            'cellphone': '2313323213',
            'condicion_iva': 'Sujeto no Categorizad',
            'tipo_factura': 'B',
            'cuit': '23256585849',
            'direccion': 'Test address',
            'pais': 'Argentina'
        }
        self.user = User(email=user_test_data.get(
            'email'), is_active=True)
        self.user.set_password(user_test_data.get('password'))
        self.user.save()

    def test_valid(self):
        """ All valid """
        Profile.objects.filter(pk=self.user.profile.id).update(
            **self.valid_profile
        )
        response = self.client.get(
            reverse('profiles:valid',
                    kwargs={
                        'user_id': self.user.id
                    }
                    )
        )
        self.assertEqual(response.json()['valid'], True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_all(self):
        """ All invalid """
        Profile.objects.filter(pk=self.user.profile.id).update(
            **self.invalid_profile
        )
        response = self.client.get(
            reverse('profiles:valid',
                    kwargs={
                        'user_id': self.user.id
                    }
                    )
        )
        self.assertEqual(response.json()['valid'], False)
        self.assertEqual(response.status_code, 200)

    def test_invalid_first_name(self):
        """ First name invalid """
        invalid_profile = self.invalid_profile.copy()
        invalid_profile['first_name'] = ''
        Profile.objects.filter(pk=self.user.profile.id).update(
            **invalid_profile
        )
        response = self.client.get(
            reverse('profiles:valid',
                    kwargs={
                        'user_id': self.user.id
                    }
                    )
        )
        self.assertEqual(response.json()['valid'], False)
        self.assertEqual(response.status_code, 200)

    def test_invalid_last_name(self):
        """ Last name invalid """
        invalid_profile = self.invalid_profile.copy()
        invalid_profile['last_name'] = ''
        Profile.objects.filter(pk=self.user.profile.id).update(
            **invalid_profile
        )
        response = self.client.get(
            reverse('profiles:valid',
                    kwargs={
                        'user_id': self.user.id
                    }
                    )
        )
        self.assertEqual(response.json()['valid'], False)
        self.assertEqual(response.status_code, 200)

    def test_invalid_nro_dni(self):
        """ nro_dni invalid """
        invalid_profile = self.invalid_profile.copy()
        invalid_profile['nro_dni'] = ''
        Profile.objects.filter(pk=self.user.profile.id).update(
            **invalid_profile
        )
        response = self.client.get(
            reverse('profiles:valid',
                    kwargs={
                        'user_id': self.user.id
                    }
                    )
        )
        self.assertEqual(response.json()['valid'], False)
        self.assertEqual(response.status_code, 200)

    def test_invalid_nro_dni(self):
        """ nro_dni invalid """
        invalid_profile = self.invalid_profile.copy()
        invalid_profile['nro_dni'] = ''
        Profile.objects.filter(pk=self.user.profile.id).update(
            **invalid_profile
        )
        response = self.client.get(
            reverse('profiles:valid',
                    kwargs={
                        'user_id': self.user.id
                    }
                    )
        )
        self.assertEqual(response.json()['valid'], False)
        self.assertEqual(response.status_code, 200)

    def test_invalid_cellphone(self):
        """ cellphone invalid """
        invalid_profile = self.invalid_profile.copy()
        invalid_profile['cellphone'] = ''
        Profile.objects.filter(pk=self.user.profile.id).update(
            **invalid_profile
        )
        response = self.client.get(
            reverse('profiles:valid',
                    kwargs={
                        'user_id': self.user.id
                    }
                    )
        )
        self.assertEqual(response.json()['valid'], False)
        self.assertEqual(response.status_code, 200)

    def test_invalid_condicion_iva(self):
        """ condicion_iva invalid """
        invalid_profile = self.invalid_profile.copy()
        invalid_profile['condicion_iva'] = ''
        Profile.objects.filter(pk=self.user.profile.id).update(
            **invalid_profile
        )
        response = self.client.get(
            reverse('profiles:valid',
                    kwargs={
                        'user_id': self.user.id
                    }
                    )
        )
        self.assertEqual(response.json()['valid'], False)
        self.assertEqual(response.status_code, 200)

    def test_invalid_tipo_factura(self):
        """ tipo_factura invalid """
        invalid_profile = self.invalid_profile.copy()
        invalid_profile['tipo_factura'] = ''
        Profile.objects.filter(pk=self.user.profile.id).update(
            **invalid_profile
        )
        response = self.client.get(
            reverse('profiles:valid',
                    kwargs={
                        'user_id': self.user.id
                    }
                    )
        )
        self.assertEqual(response.json()['valid'], False)
        self.assertEqual(response.status_code, 200)

    def test_invalid_cuit(self):
        """ cuit invalid """
        invalid_profile = self.invalid_profile.copy()
        invalid_profile['cuit'] = ''
        Profile.objects.filter(pk=self.user.profile.id).update(
            **invalid_profile
        )
        response = self.client.get(
            reverse('profiles:valid',
                    kwargs={
                        'user_id': self.user.id
                    }
                    )
        )
        self.assertEqual(response.json()['valid'], False)
        self.assertEqual(response.status_code, 200)

    def test_invalid_direccion(self):
        """ direccion invalid """
        invalid_profile = self.invalid_profile.copy()
        invalid_profile['direccion'] = ''
        Profile.objects.filter(pk=self.user.profile.id).update(
            **invalid_profile
        )
        response = self.client.get(
            reverse('profiles:valid',
                    kwargs={
                        'user_id': self.user.id
                    }
                    )
        )
        self.assertEqual(response.json()['valid'], False)
        self.assertEqual(response.status_code, 200)

    def test_invalid_pais(self):
        """ pais invalid """
        invalid_profile = self.invalid_profile.copy()
        invalid_profile['pais'] = ''
        Profile.objects.filter(pk=self.user.profile.id).update(
            **invalid_profile
        )
        response = self.client.get(
            reverse('profiles:valid',
                    kwargs={
                        'user_id': self.user.id
                    }
                    )
        )
        self.assertEqual(response.json()['valid'], False)
        self.assertEqual(response.status_code, 200)


    def test_not_exists(self):
        """ No existe el user """
        response = self.client.get(
            reverse('profiles:valid',
                    kwargs={
                        'user_id': 600
                    }
                    )
        )
        self.assertEqual(response.status_code, 204)
