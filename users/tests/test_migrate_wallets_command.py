import pytest
from io import StringIO
from users.models import User
from wallets.models import Wallet
from django.core.management import call_command


@pytest.fixture
def user():
    return User.objects.create_user('test@xcapit.com', 'test_pass')


@pytest.fixture
def wallet_for():
    def wf(an_user: User, a_network: str):
        return Wallet.objects.create(
            user=an_user,
            network=a_network,
            address=f'{a_network}_address'
        )

    return wf


@pytest.mark.django_db
def test_migrate_wallets_command(user, wallet_for):
    wallet_for(user, 'ERC20')
    wallet_for(user, 'MATIC')
    out = StringIO()
    call_command('migrate_wallets', stdout=out)
    assert 'Success' in out.getvalue()
    assert User.objects.get(email='test@xcapit.com').address == 'ERC20_address'
