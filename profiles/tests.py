import pytest
from django.urls import reverse
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer
from users.test_utils import create_user

personal_data_keys = ['first_name']
bill_data_keys = ['condicion_iva', 'tipo_factura', 'cuit', 'direccion', 'pais']
profile_keys = personal_data_keys + bill_data_keys


@pytest.fixture
def personal_data():
    return {
        'first_name': 'TestName',
        'cellphone': '3234434556'
    }


@pytest.fixture
def bill_data():
    return {
        'condicion_iva': 'Responsable Monotributo',
        'tipo_factura': 'C',
        'cuit': '39384838494',
        'direccion': 'Calle falsa 123',
        'pais': 'Argentina'
    }


@pytest.fixture
def profile_data(personal_data, bill_data):
    return {**personal_data, **bill_data}


def is_personal_data_key(key):
    return key in personal_data_keys


def is_bill_data_key(key):
    return key in bill_data_keys


@pytest.fixture
def user_data():
    return {
        'email': 'test@test.com',
        'password': 'asdfF3',
        'is_superuser': False
    }


@pytest.fixture
def profile_serializer(user_data):
    user = create_user(**user_data)
    profile = Profile.objects.get(user=user)
    return ProfileSerializer(instance=profile)


@pytest.mark.django_db
def test_profile_model_string_representation(user_data):
    user = create_user(**user_data)
    profile = Profile.objects.get(user=user)
    assert str(profile) == user_data.get('email')


@pytest.mark.django_db
def test_profile_serializer_contain_expected_fields(profile_serializer):
    data = profile_serializer.data
    print(data.keys())
    # Add email and cellphone because it is not used for profile valid, so not in profile_keys
    assert len(data.keys()) == len(profile_keys + ['email', 'cellphone'])


@pytest.mark.django_db
def test_profile_serializer_email_field_content(profile_serializer, user_data):
    data = profile_serializer.data
    assert data.get('email') == user_data.get('email')


def test_profile_serializer_valid(profile_data):
    serializer = ProfileSerializer(data=profile_data)
    assert serializer.is_valid(raise_exception=False) is True


def test_profile_serializer_invalid():
    serializer = ProfileSerializer(data={'asdas': 'asdas'})
    assert serializer.is_valid(raise_exception=False) is False


@pytest.mark.django_db
def test_personal_data_api_view(client, personal_data):
    user = create_user('test@test.com', 'TestPass1234', False)
    url = reverse('profiles:user-profile-personal-data', kwargs={'user_id': user.id})
    response = client.put(url, data=personal_data, content_type='application/json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.parametrize('field', ['first_name'])
def test_personal_data_api_view_invalid_data(client, personal_data, field):
    temp = personal_data.copy()
    temp.pop(field)
    invalid_personal_data = temp.copy()
    user = create_user('test@test.com', 'TestPass1234', False)
    url = reverse('profiles:user-profile-personal-data', kwargs={'user_id': user.id})
    response = client.put(url, data=invalid_personal_data, content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert field in response.json()
    assert response.json()['error_code'] == 'profiles.update.invalidData'


@pytest.mark.django_db
def test_personal_data_api_view_profile_not_exists(client, personal_data):
    url = reverse('profiles:user-profile-personal-data', kwargs={'user_id': 50})
    response = client.put(url, data=personal_data, content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error_code'] == 'profiles.update.doesNotExists'


@pytest.mark.django_db
def test_bill_data_api_view(client, bill_data):
    user = create_user('test@test.com', 'TestPass1234', False)
    url = reverse('profiles:user-profile-bill-data', kwargs={'user_id': user.id})
    response = client.put(url, data=bill_data, content_type='application/json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.parametrize('field', ['condicion_iva', 'tipo_factura', 'cuit', 'direccion', 'pais'])
def test_bill_data_api_view_invalid_data(client, bill_data, field):
    temp = bill_data.copy()
    temp.pop(field)
    invalid_bill_data = temp.copy()
    user = create_user('test@test.com', 'TestPass1234', False)
    url = reverse('profiles:user-profile-bill-data', kwargs={'user_id': user.id})
    response = client.put(url, data=invalid_bill_data, content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert field in response.json()
    assert response.json()['error_code'] == 'profiles.update.invalidData'


@pytest.mark.django_db
def test_bill_data_api_view_profile_not_exists(client, bill_data):
    url = reverse('profiles:user-profile-bill-data', kwargs={'user_id': 50})
    response = client.put(url, data=bill_data, content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error_code'] == 'profiles.update.doesNotExists'


@pytest.mark.django_db
def test_put_profile_data_api_view(client, profile_data):
    user = create_user('test@test.com', 'TestPass1234', False)
    url = reverse('profiles:retrieve-update-user-profile', kwargs={'user_id': user.id})
    response = client.put(url, data=profile_data, content_type='application/json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.parametrize('field', profile_keys)
def test_put_profile_data_api_view_invalid_data(client, profile_data, field):
    temp = profile_data.copy()
    temp.pop(field)
    invalid_profile_data = temp.copy()
    user = create_user('test@test.com', 'TestPass1234', False)
    url = reverse('profiles:retrieve-update-user-profile', kwargs={'user_id': user.id})
    response = client.put(url, data=invalid_profile_data, content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert field in response.json()
    assert response.json()['error_code'] == 'profiles.update.invalidData'


@pytest.mark.django_db
def test_put_profile_data_api_view_profile_not_exists(client, profile_data):
    url = reverse('profiles:retrieve-update-user-profile', kwargs={'user_id': 50})
    response = client.put(url, data=profile_data, content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error_code'] == 'profiles.update.doesNotExists'


@pytest.mark.django_db
def test_get_profile_data_api_view(client):
    user = create_user('test@test.com', 'TestPass1234', False)
    url = reverse('profiles:retrieve-update-user-profile', kwargs={'user_id': user.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_profile_data_api_view_profile_not_exists(client, profile_data):
    url = reverse('profiles:retrieve-update-user-profile', kwargs={'user_id': 50})
    response = client.put(url, data=profile_data, content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error_code'] == 'profiles.update.doesNotExists'


@pytest.mark.django_db
@pytest.mark.parametrize(
    'key, valid',
    [(key, not is_personal_data_key(key)) for key in profile_keys]
)
def test_profile_valid_validate_personal_data(client, key, valid, profile_data):
    profile_data_without_key = profile_data.copy()
    profile_data_without_key[key] = ''
    user = create_user('test@test.com', 'TestPass1234', False)
    Profile.objects.filter(user_id=user.id).update(**profile_data_without_key)
    url = reverse('profiles:valid', kwargs={'user_id': user.id})
    response = client.get(url, {'validation_type': 'personal_data'}, )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['valid'] == valid


@pytest.mark.django_db
@pytest.mark.parametrize(
    'key, valid',
    [(key, not is_bill_data_key(key)) for key in profile_keys]
)
def test_profile_valid_validate_bill_data(client, key, valid, profile_data):
    profile_data_without_key = profile_data.copy()
    profile_data_without_key[key] = ''
    user = create_user('test@test.com', 'TestPass1234', False)
    Profile.objects.filter(user_id=user.id).update(**profile_data_without_key)
    url = reverse('profiles:valid', kwargs={'user_id': user.id})
    response = client.get(url, {'validation_type': 'bill_data'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['valid'] == valid


@pytest.mark.django_db
@pytest.mark.parametrize(
    'key, valid',
    [(key, not is_personal_data_key(key)) for key in profile_keys]
)
def test_profile_valid(client, key, valid, profile_data):
    profile_data_without_key = profile_data.copy()
    profile_data_without_key[key] = ''
    user = create_user('test@test.com', 'TestPass1234', False)
    Profile.objects.filter(user_id=user.id).update(**profile_data_without_key)
    url = reverse('profiles:valid', kwargs={'user_id': user.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['valid'] == valid
