import pytest
import pandas as pd
from users.models import User
from wallets.models import Wallet
from referrals.models import Referral


@pytest.fixture
def users_for_referrals_case_1():
    return [
        {'email': 'user@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_user'},
        {'email': 'for_1@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_for_1'},
        {'email': 'for_2@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_for_2'},
        {'email': 'for_3@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_for_3'},
        {'email': 'for_4@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_for_4'},
        {'email': 'sor_11@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_sor_11'},
        {'email': 'sor_12@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_sor_12'},
        {'email': 'sor_13@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_sor_13'},
        {'email': 'sor_31@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_sor_31'},
        {'email': 'sor_32@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_sor_32'},
        {'email': 'sor_33@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_sor_33'},
        {'email': 'sor_34@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_sor_34'},
    ]


@pytest.fixture
def users_for_referrals_case_zero_second_level():
    return [
        {'email': 'user@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_user'},
        {'email': 'for_1@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_for_1'},
        {'email': 'for_2@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_for_2'},
    ]


@pytest.fixture
def wallets_for_referrals_case_1():
    return [
        [
            {'user_id': user_id, 'network': 'MATIC', 'address': 'test_matic_address'},
            {'user_id': user_id, 'network': 'RSK', 'address': 'test_rsk_address'},
            {'user_id': user_id, 'network': 'ERC20', 'address': 'test_erc20_address'},
        ]
        for user_id in ['1', '2', '5', '6', '8', '9']
    ]


@pytest.fixture
def wallets_for_referrals_case_zero_second_level():
    return [
        [
            {'user_id': user_id, 'network': 'MATIC', 'address': 'test_matic_address'},
            {'user_id': user_id, 'network': 'RSK', 'address': 'test_rsk_address'},
            {'user_id': user_id, 'network': 'ERC20', 'address': 'test_erc20_address'},
        ]
        for user_id in ['1', '2']
    ]


@pytest.fixture
def referrals_for_case_1():
    return [
        {'accepted': True, 'referral_id': 'rid_user', 'email': 'for_1@test.com'},
        {'accepted': True, 'referral_id': 'rid_user', 'email': 'for_2@test.com'},
        {'accepted': True, 'referral_id': 'rid_user', 'email': 'for_3@test.com'},
        {'accepted': True, 'referral_id': 'rid_user', 'email': 'for_4@test.com'},

        {'accepted': True, 'referral_id': 'rid_for_1', 'email': 'sor_11@test.com'},
        {'accepted': True, 'referral_id': 'rid_for_1', 'email': 'sor_12@test.com'},
        {'accepted': True, 'referral_id': 'rid_for_1', 'email': 'sor_13@test.com'},

        {'accepted': True, 'referral_id': 'rid_for_3', 'email': 'sor_31@test.com'},
        {'accepted': True, 'referral_id': 'rid_for_3', 'email': 'sor_32@test.com'},
        {'accepted': True, 'referral_id': 'rid_for_3', 'email': 'sor_33@test.com'},
        {'accepted': False, 'referral_id': 'rid_for_3', 'email': 'sor_34@test.com'},
    ]


@pytest.fixture
def referrals_for_case_zero_second_level():
    return [
        {'accepted': True, 'referral_id': 'rid_user', 'email': 'for_1@test.com'},
        {'accepted': True, 'referral_id': 'rid_user', 'email': 'for_2@test.com'},
    ]


@pytest.fixture
def set_referrals_fixtures():
    def srf(users, wallets, referrals):
        for user in users:
            rid = user.pop('referral_id')
            user = User.objects.create_user(**user)
            user.referral_id = rid
            user.save()
        for user_wallets in wallets:
            for user_wallet in user_wallets:
                Wallet.objects.create(**user_wallet)
        for referral in referrals:
            Referral.objects.create(**referral)

    return srf


@pytest.fixture
def set_fixtures_referrals_case_1(users_for_referrals_case_1, wallets_for_referrals_case_1, referrals_for_case_1):
    def sfr_case_1():
        return set_referrals_fixtures(
            users_for_referrals_case_1,
            wallets_for_referrals_case_1,
            referrals_for_case_1
        )

    return sfr_case_1


@pytest.fixture
def set_fixtures_referrals_case_zero():
    def sfr_case_zfl():
        user = User.objects.create_user('test_zero@test.com', 'TestPass1234')
        user.referral_id = 'rid_test_zero'
        user.save()

    return sfr_case_zfl


@pytest.fixture
def set_fixtures_referrals_case_zero_second_level(
        set_referrals_fixtures,
        users_for_referrals_case_zero_second_level,
        wallets_for_referrals_case_zero_second_level,
        referrals_for_case_zero_second_level
):
    def sfr_case_zsl():
        return set_referrals_fixtures(
            users_for_referrals_case_zero_second_level,
            wallets_for_referrals_case_zero_second_level,
            referrals_for_case_zero_second_level
        )

    return sfr_case_zsl


@pytest.fixture
def expected_first_level():
    return pd.DataFrame(
        data={
            'referred_id': ['rid_for_1', 'rid_for_2', 'rid_for_3', 'rid_for_4'],
            'referral_id': ['rid_user', 'rid_user', 'rid_user', 'rid_user'],
            'wallet_created': [True, False, False, True],
            'user_id': [2, 3, 4, 5]
        }
    ).set_index('user_id')


@pytest.fixture
def expected_second_level():
    return pd.DataFrame(
        data={
            'referred_id': ['rid_sor_11', 'rid_sor_12', 'rid_sor_13', 'rid_sor_31', 'rid_sor_32', 'rid_sor_33'],
            'referral_id': ['rid_for_1', 'rid_for_1', 'rid_for_1', 'rid_for_3', 'rid_for_3', 'rid_for_3'],
            'wallet_created': [True, False, True, True, False, False],
            'user_id': [6, 7, 8, 9, 10, 11]
        }
    ).set_index('user_id')


@pytest.fixture
def expected_referrals_case_zero_second_level():
    return pd.DataFrame(
        data={
            'referred_id': ['rid_for_1', 'rid_for_2'],
            'referral_id': ['rid_user', 'rid_user'],
            'wallet_created': [True, False],
            'user_id': [2, 3]
        }
    ).set_index('user_id')


@pytest.fixture
def expected_user_referrals():
    return {
        "first_order": {"with_wallet": 2, "without_wallet": 2, "reward": 1},
        "second_order": {"with_wallet": 3, "without_wallet": 3, "reward": 0.5}
    }


@pytest.fixture
def expected_user_zero_referrals():
    return {
        "first_order": {"with_wallet": 0, "without_wallet": 0, "reward": 1},
        "second_order": {"with_wallet": 0, "without_wallet": 0, "reward": 0.5}
    }


@pytest.fixture
def expected_user_referrals_zero_second_level():
    return {
        "first_order": {"with_wallet": 1, "without_wallet": 1, "reward": 1},
        "second_order": {"with_wallet": 0, "without_wallet": 0, "reward": 0.5}
    }
