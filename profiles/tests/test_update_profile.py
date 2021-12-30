import pytest
from django.urls import reverse
from profiles.models import Profile
from users.models import User


@pytest.mark.wip
@pytest.mark.django_db
def test_update_notifications_enabled_patch(client):
    user = User.objects.create_user('test', 'test')
    assert user.profile.notifications_enabled
    response = client.patch(
        reverse('profiles:retrieve-update-user-profile', kwargs={'user_id': 1}),
        data={'notifications_enabled': False},
        content_type='application/json'
    )
    assert response.status_code == 200
    assert not Profile.objects.get(user_id=user.id).notifications_enabled


@pytest.mark.wip
@pytest.mark.django_db
def test_update_notifications_enabled_patch_invalid(client):
    User.objects.create_user('test', 'test')
    response = client.patch(
        reverse('profiles:retrieve-update-user-profile', kwargs={'user_id': 1}),
        data={'notifications_enabled': 'yes, sure'},
        content_type='application/json'
    )
    assert response.status_code == 400
