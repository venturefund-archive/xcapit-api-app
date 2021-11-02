import pytest
from users.models import User
from wallets.models import NFTRequest


@pytest.fixture
def user_mock():
    return User.objects.create_user(email='test', password='TestPass123')


@pytest.fixture
def nft_request_mock():
    def nrm(user: User):
        return NFTRequest.objects.create(user=user)

    return nrm
