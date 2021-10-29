import pytest
from datetime import datetime
from django.urls import reverse
from wallets.models import NFTRequest


@pytest.mark.django_db
def test_create_nft_request_view(client, user_mock):
    response = client.post(
        reverse('wallets:create-nft-request', kwargs={'user_id': user_mock.id}),
        content_type='application/json'
    )
    created_request = NFTRequest.objects.filter(user=user_mock).first()
    assert response.status_code == 200
    assert created_request.user == user_mock
    assert created_request.status == 'claimed'
    assert created_request.claimed_at.date() == datetime.now().date()


@pytest.mark.django_db
def test_create_nft_request_view_non_existing_user(client, user_mock):
    non_existing_user_id = 4123
    response = client.post(
        reverse('wallets:create-nft-request', kwargs={'user_id': non_existing_user_id}),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.json()['user'] == [f'Invalid pk "{non_existing_user_id}" - object does not exist.']
