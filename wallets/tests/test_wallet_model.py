import pytest
from users.models import User
from wallets.models import Wallet
from django.db import IntegrityError


@pytest.fixture
def user_mock():
    return User.objects.create_user(email='test', password='TestPass123')


@pytest.mark.django_db
def test_wallet_model(user_mock):
    wallet = Wallet.objects.create(user=user_mock, network='ERC20', address='test_address')
    assert wallet.user == user_mock
    assert wallet.network == 'ERC20'
    assert wallet.address == 'test_address'


@pytest.mark.django_db
def test_wallet_model_unique(user_mock):
    with pytest.raises(IntegrityError) as e:
        Wallet.objects.create(user=user_mock, network='ERC20', address='test_address')
        Wallet.objects.create(user=user_mock, network='ERC20', address='test_address')
        assert e
