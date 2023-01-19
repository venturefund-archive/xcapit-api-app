import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_user_wallets_view_success(client, user_mock, wallet_mock, expected_user_wallets):
    user = user_mock
    user.address = f'test_erc20_address_{user.id}'
    user.save()
    wallet_mock(user_mock)
    response = client.get(
        reverse('wallets:user-wallet-address', kwargs={'wallet_address': user.address}))
    assert response.json() == expected_user_wallets(user_mock)


@pytest.mark.django_db
def test_get_user_wallets_view_error(client):
    response = client.get(
        reverse('wallets:user-wallet-address', kwargs={'wallet_address': '0xnonExistentWallet'}))
    assert response.json() == {'error': 'wallet address does not exist in BD'}
