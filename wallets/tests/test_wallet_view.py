import pytest
from django.urls import reverse
from users.models import User
from wallets.models import Wallet


@pytest.fixture
def wallets_data():
    return [
        {'network': 'ERC20', 'address': 'test_erc20_address'},
        {'network': 'RSK', 'address': 'test_rsk_address'},
        {'network': 'MATIC', 'address': 'test_matic_address'},
    ]


@pytest.fixture
def wallets_data2():
    return [
        {'network': 'ERC20', 'address': 'test_erc20_address2'},
        {'network': 'RSK', 'address': 'test_rsk_address2'},
        {'network': 'MATIC', 'address': 'test_matic_address2'},
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
    assert User.objects.get(pk=user_mock.id).address == 'test_erc20_address'


@pytest.mark.django_db
def test_wallet_view_with_existing_wallets(client, user_mock, wallets_data, wallets_data2):
    response_1 = client.post(
        reverse('wallets:wallets', kwargs={'user_id': user_mock.id}),
        data=wallets_data,
        content_type='application/json'
    )
    assert response_1.status_code == 200
    response_2 = client.post(
        reverse('wallets:wallets', kwargs={'user_id': user_mock.id}),
        data=wallets_data2,
        content_type='application/json'
    )
    assert response_2.status_code == 200
    wallets = Wallet.objects.all()
    assert wallets.count() == 3
    assert wallets.filter(user_id='1', network='ERC20').first().address == 'test_erc20_address2'
    assert wallets.filter(user_id='1', network='RSK').first().address == 'test_rsk_address2'
    assert wallets.filter(user_id='1', network='MATIC').first().address == 'test_matic_address2'
    assert User.objects.get(pk=user_mock.id).address == 'test_erc20_address2'


@pytest.mark.django_db
def test_wallet_view_invalid_data(client, user_mock, wallets_data):
    wallets_data[0].pop('network')
    response = client.post(
        reverse('wallets:wallets', kwargs={'user_id': user_mock.id}),
        data=wallets_data,
        content_type='application/json'
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_claimed_nft_users_case_all_users_claimed_the_nft(
        client, wallet_and_nft_case_all_users_have_wallet_and_already_claimed_nft,
        expected_claimed_users_case_all_users_have_wallet_and_already_claimed_nft):
    response = client.get(reverse('wallets:users-who-claimed-nft'))

    assert response.json() == expected_claimed_users_case_all_users_have_wallet_and_already_claimed_nft
    assert response.status_code == 200


@pytest.mark.django_db
def test_claimed_nft_users_case_some_users_claimed_the_nft(
        client, wallet_and_nft_case_some_users_have_wallet_and_already_claimed_nft,
        expected_claimed_users_case_some_users_have_wallet_and_already_claimed_nft):
    response = client.get(reverse('wallets:users-who-claimed-nft'))

    assert response.json() == expected_claimed_users_case_some_users_have_wallet_and_already_claimed_nft
    assert response.status_code == 200


@pytest.mark.django_db
def test_claimed_nft_users_case_no_claims(client, wallet_and_nft_case_no_claims, expected_claimed_users_case_no_claims):
    response = client.get(reverse('wallets:users-who-claimed-nft'))

    assert response.json() == expected_claimed_users_case_no_claims
    assert response.status_code == 200


@pytest.mark.django_db
def test_wallets_api_view(client, wallet_mock_with_default_user):
    wallet_mock_with_default_user()
    response = client.get(reverse('wallets:wallets'), {"page_size": 1})
    assert response.status_code == 200
    assert response.json()['results'] == [{"network": "ERC20", "address": "test_erc20_address"}]
