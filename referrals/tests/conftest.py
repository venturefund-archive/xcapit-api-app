import pytz
import pytest
import datetime
import pandas as pd
from unittest import mock
from users.models import User
from wallets.models import Wallet
from referrals.models import Referral


def create_with_utc(df: pd.DataFrame):
    df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%d %H:%M:%S', utc=True)
    return df


@pytest.fixture
def empty_next_level():
    return pd.DataFrame(
        columns=['referred_id', 'user_id', 'referral_id', 'created_at', 'wallet_created']
    ).set_index('user_id')


@pytest.fixture
def set_referrals_fixtures():
    def srf(users, wallets, referrals):
        mocked = datetime.datetime(2021, 4, 4, 21, 30, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
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
def users_for_referrals_case_2():
    return [
        {'email': 'bhai.them.756m@bookeg.site', 'password': 'TestPass1234', 'referral_id': 'avVYfJ'},
        {'email': 'gamin_myhero.009a@oanghika.com', 'password': 'TestPass1234', 'referral_id': 'e262s9'},
    ]


@pytest.fixture
def users_for_referrals_case_zero_second_level():
    return [
        {'email': 'user@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_user'},
        {'email': 'for_1@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_for_1'},
        {'email': 'for_2@test.com', 'password': 'TestPass1234', 'referral_id': 'rid_for_2'},
    ]


@pytest.fixture
def referrals_for_case_1():
    return [
        {'accepted': True, 'referral_id': 'rid_user', 'email': 'for_1@test.com', 'created_at': '2021-04-04 21:30:00'},
        {'accepted': True, 'referral_id': 'rid_user', 'email': 'for_2@test.com', 'created_at': '2021-04-04 21:30:00'},
        {'accepted': True, 'referral_id': 'rid_user', 'email': 'for_3@test.com', 'created_at': '2021-04-04 21:30:00'},
        {'accepted': True, 'referral_id': 'rid_user', 'email': 'for_4@test.com', 'created_at': '2021-04-04 21:30:00'},

        {'accepted': True, 'referral_id': 'rid_for_1', 'email': 'sor_11@test.com', 'created_at': '2021-04-04 21:30:00'},
        {'accepted': True, 'referral_id': 'rid_for_1', 'email': 'sor_12@test.com', 'created_at': '2021-04-04 21:30:00'},
        {'accepted': True, 'referral_id': 'rid_for_1', 'email': 'sor_13@test.com', 'created_at': '2021-04-04 21:30:00'},

        {'accepted': True, 'referral_id': 'rid_for_3', 'email': 'sor_31@test.com', 'created_at': '2021-04-04 21:30:00'},
        {'accepted': True, 'referral_id': 'rid_for_3', 'email': 'sor_32@test.com', 'created_at': '2021-04-04 21:30:00'},
        {'accepted': True, 'referral_id': 'rid_for_3', 'email': 'sor_33@test.com', 'created_at': '2021-04-04 21:30:00'},
        {'accepted': False, 'referral_id': 'rid_for_3', 'email': 'sor_34@test.com', 'created_at': '2021-04-04 21:30:00'},
    ]


@pytest.fixture
def referrals_for_case_2():
    return [{'accepted': True, 'referral_id': 'avVYfJ', 'email': 'gamin_myhero.009a@oanghika.com', 'created_at': '2021-04-04 21:30:00'}]


@pytest.fixture
def referrals_for_case_zero_second_level():
    return [
        {'accepted': True, 'referral_id': 'rid_user', 'email': 'for_1@test.com', 'created_at': '2021-04-04 21:30:00'},
        {'accepted': True, 'referral_id': 'rid_user', 'email': 'for_2@test.com', 'created_at': '2021-04-04 21:30:00'},
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
def wallets_for_referrals_case_2():
    return [
        [
            {'user_id': user_id, 'network': 'MATIC', 'address': 'test_matic_address'},
            {'user_id': user_id, 'network': 'RSK', 'address': 'test_rsk_address'},
            {'user_id': user_id, 'network': 'ERC20', 'address': 'test_erc20_address'},
        ]
        for user_id in ['1', '2']
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
def set_fixtures_referrals_case_1(
        set_referrals_fixtures,
        users_for_referrals_case_1,
        wallets_for_referrals_case_1,
        referrals_for_case_1
):
    def sfr_case_1():
        return set_referrals_fixtures(
            users_for_referrals_case_1,
            wallets_for_referrals_case_1,
            referrals_for_case_1
        )

    return sfr_case_1


@pytest.fixture
def set_fixtures_referrals_case_2(
        set_referrals_fixtures,
        users_for_referrals_case_2,
        wallets_for_referrals_case_2,
        referrals_for_case_2
):
    def sfr_case_2():
        return set_referrals_fixtures(
            users_for_referrals_case_2,
            wallets_for_referrals_case_2,
            referrals_for_case_2
        )

    return sfr_case_2


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
    first_level_result = pd.DataFrame(
        data={
            'referred_id': ['rid_for_1', 'rid_for_2', 'rid_for_3', 'rid_for_4'],
            'referral_id': ['rid_user', 'rid_user', 'rid_user', 'rid_user'],
            'created_at': ['2021-04-04 21:30:00', '2021-04-04 21:30:00', '2021-04-04 21:30:00', '2021-04-04 21:30:00'],
            'wallet_created': [True, False, False, True],
            'user_id': [2, 3, 4, 5]
        }
    ).set_index('user_id')

    first_level_result['created_at'] = pd.to_datetime(first_level_result['created_at'], format='%Y-%m-%d %H:%M:%S')

    return first_level_result


@pytest.fixture
def expected_second_level():
    second_level_result = pd.DataFrame(
        data={
            'referred_id': ['rid_sor_11', 'rid_sor_12', 'rid_sor_13', 'rid_sor_31', 'rid_sor_32', 'rid_sor_33'],
            'referral_id': ['rid_for_1', 'rid_for_1', 'rid_for_1', 'rid_for_3', 'rid_for_3', 'rid_for_3'],
            'created_at': ['2021-04-04 21:30:00', '2021-04-04 21:30:00', '2021-04-04 21:30:00', '2021-04-04 21:30:00', '2021-04-04 21:30:00', '2021-04-04 21:30:00'],
            'wallet_created': [True, False, True, True, False, False],
            'user_id': [6, 7, 8, 9, 10, 11]
        }
    ).set_index('user_id')

    second_level_result['created_at'] = pd.to_datetime(second_level_result['created_at'], format='%Y-%m-%d %H:%M:%S')

    return second_level_result


@pytest.fixture
def expected_referrals_case_zero_second_level():
    zero_second_level_result = pd.DataFrame(
        data={
            'referred_id': ['rid_for_1', 'rid_for_2'],
            'referral_id': ['rid_user', 'rid_user'],
            'created_at': ['2021-04-04 21:30:00', '2021-04-04 21:30:00'],
            'wallet_created': [True, False],
            'user_id': [2, 3]
        }
    ).set_index('user_id')

    zero_second_level_result['created_at'] = pd.to_datetime(zero_second_level_result['created_at'], format='%Y-%m-%d %H:%M:%S')

    return zero_second_level_result


@pytest.fixture
def expected_referrals_case_case_2_level_one():
    zero_second_level_result = pd.DataFrame(
        data={
            'referred_id': ['rid_for_1'],
            'referral_id': ['rid_user'],
            'created_at': ['2021-04-04 21:30:00'],
            'wallet_created': [False],
            'user_id': [2]
        }
    ).set_index('user_id')

    zero_second_level_result['created_at'] = pd.to_datetime(zero_second_level_result['created_at'], format='%Y-%m-%d %H:%M:%S')

    return zero_second_level_result



@pytest.fixture
def expected_user_referrals():
    return {
        "first_order": {"with_wallet": 0, "without_wallet": 4, "reward": 1},
        "second_order": {"with_wallet": 0, "without_wallet": 3, "reward": 0.5}
    }


@pytest.fixture
def expected_user_referrals_case_2():
    return {
        "first_order": {"with_wallet": 0, "without_wallet": 1, "reward": 1},
        "second_order": {"with_wallet": 0, "without_wallet": 0, "reward": 0.5}
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
        "first_order": {"with_wallet": 0, "without_wallet": 2, "reward": 1},
        "second_order": {"with_wallet": 0, "without_wallet": 0, "reward": 0.5}
    }


@pytest.fixture
def raw_token():
    return 'token'
