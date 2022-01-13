import pytest
from django.urls import reverse
from profiles.models import Profile
from users.models import User


@pytest.mark.django_db
def test_update_notifications_enabled_patch(client, test_user):
    assert test_user.profile.notifications_enabled
    response = client.patch(
        reverse('profiles:retrieve-update-user-profile', kwargs={'user_id': 1}),
        data={'notifications_enabled': False},
        content_type='application/json'
    )
    assert response.status_code == 200
    assert not Profile.objects.get(user_id=test_user.id).notifications_enabled


@pytest.mark.django_db
def test_update_notifications_enabled_patch_invalid(client, test_user):
    response = client.patch(
        reverse('profiles:retrieve-update-user-profile', kwargs={'user_id': 1}),
        data={'notifications_enabled': 'yes, sure'},
        content_type='application/json'
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_update_investor_score_patch(client, test_user):
    response = client.patch(
        reverse('profiles:retrieve-update-user-profile', kwargs={'user_id': 1}),
        data={'investor_score': 6},
        content_type='application/json'
    )
    assert response.status_code == 200
    assert Profile.objects.get(user_id=test_user.id).investor_score == 6


@pytest.mark.django_db
def test_update_investor_score_patch_invalid(client, test_user):
    response = client.patch(
        reverse('profiles:retrieve-update-user-profile', kwargs={'user_id': 1}),
        data={'investor_score': 19},
        content_type='application/json'
    )
    assert response.status_code == 400
