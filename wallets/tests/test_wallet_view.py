import pytest
from django.urls import reverse

from wallets.models import Wallet


@pytest.fixture
def wallets_data():
    return [
        {'network': 'ERC20', 'address': 'test_erc20_address'},
        {'network': 'RSK', 'address': 'test_rsk_address'},
        {'network': 'MATIC', 'address': 'test_matic_address'},
    ]


@pytest.mark.django_db
def test_wallet_view(client, user_mock, wallets_data):
    response = client.post(
        reverse('wallets:wallets', kwargs={'user_id': user_mock.id}),
        data=wallets_data,
        content_type='application/json'
    )
    assert response.status_code == 200
    wallets = Wallet.objects.all()
    assert wallets.filter(user=user_mock).count() == 3
    assert wallets.filter(network='ERC20').first().address == 'test_erc20_address'
    assert wallets.filter(network='RSK').first().address == 'test_rsk_address'
    assert wallets.filter(network='MATIC').first().address == 'test_matic_address'


@pytest.mark.django_db
def test_wallet_view_with_existing_wallets(client, user_mock, wallets_data):
    response_1 = client.post(
        reverse('wallets:wallets', kwargs={'user_id': user_mock.id}),
        data=wallets_data,
        content_type='application/json'
    )
    assert response_1.status_code == 200
    response_2 = client.post(
        reverse('wallets:wallets', kwargs={'user_id': user_mock.id}),
        data=wallets_data,
        content_type='application/json'
    )
    assert response_2.status_code == 200
    wallets = Wallet.objects.all()
    assert wallets.count() == 3
    assert wallets.filter(network='ERC20').first().address == 'test_erc20_address'
    assert wallets.filter(network='RSK').first().address == 'test_rsk_address'
    assert wallets.filter(network='MATIC').first().address == 'test_matic_address'


@pytest.mark.django_db
def test_wallet_view_invalid_data(client, user_mock, wallets_data):
    wallets_data[0].pop('network')
    response = client.post(
        reverse('wallets:wallets', kwargs={'user_id': user_mock.id}),
        data=wallets_data,
        content_type='application/json'
    )
    assert response.status_code == 400
