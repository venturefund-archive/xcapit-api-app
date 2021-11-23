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
        wallets = [{"user": user, "network": "ERC20", "address": "test_address"},
                   {"user": user, "network": "MATIC", "address": "test_address"},
                   {"user": user, "network": "RSK", "address": "test_address"}]
        for wallet in wallets:
            Wallet.objects.create(**wallet)
        return

    return wm


@pytest.fixture
def wallet_and_nft_case_one(wallet_mock, nft_request_mock, user_mock, user_mock2):
    wallet_mock(user_mock)
    wallet_mock(user_mock2)
    nft_request_mock(user_mock)
    nft_request_mock(user_mock2)
    return


@pytest.fixture
def wallet_and_nft_case_two(wallet_mock, nft_request_mock, user_mock, user_mock2):
    wallet_mock(user_mock)
    wallet_mock(user_mock2)
    nft_request_mock(user_mock)
    nft_request_mock(user_mock2, status='delivered')
    return


@pytest.fixture
def wallet_and_nft_case_no_claims(wallet_mock, nft_request_mock, user_mock, user_mock2):
    wallet_mock(user_mock)
    wallet_mock(user_mock2)
    return


@pytest.fixture
def expected_claimed_users_case_one():
    return [{'id': 1, 'email': 'test', 'address': 'test_address'},
            {'id': 2, 'email': 'test2', 'address': 'test_address'}, ]


@pytest.fixture
def expected_claimed_users_case_two():
    return [{'id': 1, 'email': 'test', 'address': 'test_address'}]


@pytest.fixture
def expected_claimed_users_case_no_claims():
    return []
