from io import StringIO

import pytest
from django.core.management import call_command

from users.models import User
from wallets.models import Wallet


@pytest.mark.django_db
def test_wallets_lowercase_command(user_mock, wallet_for):
    wallet_for(user_mock, 'ERC20')
    wallet_for(user_mock, 'MATIC')
    wallet_for(user_mock, 'SOLANA')
    out = StringIO()

    call_command('wallets_lowercase', stdout=out)

    assert 'Success' in out.getvalue()
    assert Wallet.objects.filter(user_id=user_mock.id, address='erc20_address').exists()
    assert Wallet.objects.filter(user_id=user_mock.id, address='SOLANA_address').exists()
    assert User.objects.get(id=user_mock.id).address == 'erc20_address'
