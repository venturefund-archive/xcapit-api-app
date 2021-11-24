import pytest
from users.models import User
from wallets.models import NFTRequest, Wallet


@pytest.fixture
def user_mock():
    return User.objects.create_user(email='test', password='TestPass123')


@pytest.fixture
def user_mock2():
    return User.objects.create_user(email='test2', password='TestPass123')


@pytest.fixture
def nft_request_mock():
    def nrm(user: User, status="claimed"):
        return NFTRequest.objects.create(user=user, status=status)

    return nrm


@pytest.fixture
def wallet_mock():
    def wm(user: User):
        wallets = [{"user": user, "network": "ERC20", "address": f"test_erc20_address_{user.id}"},
                   {"user": user, "network": "MATIC", "address": f"test_matic_address_{user.id}"},
                   {"user": user, "network": "RSK", "address": f"test_rsk_address_{user.id}"}]
        for wallet in wallets:
            Wallet.objects.create(**wallet)
        return

    return wm


@pytest.fixture
def wallet_and_nft_case_all_users_have_wallet_and_already_claimed_nft(wallet_mock, nft_request_mock, user_mock,
                                                                      user_mock2):
    wallet_mock(user_mock)
    wallet_mock(user_mock2)
    nft_request_mock(user_mock)
    nft_request_mock(user_mock2)


@pytest.fixture
def wallet_and_nft_case_some_users_have_wallet_and_already_claimed_nft(wallet_mock, nft_request_mock, user_mock,
                                                                       user_mock2):
    wallet_mock(user_mock)
    wallet_mock(user_mock2)
    nft_request_mock(user_mock)
    nft_request_mock(user_mock2, status='delivered')


@pytest.fixture
def wallet_and_nft_case_no_claims(wallet_mock, nft_request_mock, user_mock, user_mock2):
    wallet_mock(user_mock)
    wallet_mock(user_mock2)


@pytest.fixture
def expected_claimed_users_case_all_users_have_wallet_and_already_claimed_nft():
    return [{'id': 1, 'email': 'test', 'address': 'test_matic_address_1'},
            {'id': 2, 'email': 'test2', 'address': 'test_matic_address_2'}, ]


@pytest.fixture
def expected_claimed_users_case_some_users_have_wallet_and_already_claimed_nft():
    return [{'id': 1, 'email': 'test', 'address': 'test_matic_address_1'}]


@pytest.fixture
def expected_claimed_users_case_no_claims():
    return []
