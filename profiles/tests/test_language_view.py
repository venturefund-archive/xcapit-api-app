import pytest
from django.urls import reverse
from profiles.models import Profile
from users.models import User


@pytest.mark.django_db
def test_language_view(client, language_mock):
    user = User.objects.create_user('test@test.com', 'test')
    assert Profile.objects.get(user__id=user.id).lang == 'es'
    url = reverse('profiles:language', kwargs={'user_id': user.id})
    response = client.put(url, data=language_mock, content_type='application/json')
    assert response.status_code == 200
    assert Profile.objects.get(user__id=user.id).lang == 'en'


@pytest.mark.django_db
def test_language_view_not_exists(client, language_mock):
    url = reverse('profiles:language', kwargs={'user_id': 23})
    response = client.put(url, data=language_mock, content_type='application/json')
    assert response.status_code == 404
