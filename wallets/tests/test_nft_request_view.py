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


@pytest.mark.django_db
def test_nft_status_view(client, user_mock, nft_request_mock):
    nft_request_mock(user_mock)
    response = client.get(reverse('wallets:nft-status', kwargs={'user_id': user_mock.id}))
    assert response.status_code == 200
    response = response.json()
    assert response['user'] == user_mock.id
    assert response['status'] == 'claimed'
    assert response['claimed_at']


@pytest.mark.django_db
def test_update_nft_request(client, user_mock, nft_request_mock):
    nft_request_mock(user_mock)
    assert NFTRequest.objects.get(user__id=user_mock.id).status == 'claimed'
    url = reverse('wallets:create-nft-request', kwargs={'user_id': user_mock.id})
    response = client.put(url, data={'status': 'delivered'}, content_type='application/json')
    assert response.status_code == 200
    assert NFTRequest.objects.get(user__id=user_mock.id).status == 'delivered'


@pytest.mark.django_db
def test_update_nft_request_user_doesnt_exist(client):
    url = reverse('wallets:create-nft-request', kwargs={'user_id': 45})
    response = client.put(url, data={'status': 'delivered'}, content_type='application/json')
    assert response.status_code == 404
