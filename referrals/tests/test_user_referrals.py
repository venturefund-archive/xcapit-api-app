import pytest
from referrals.next_level_referrals import DefaultNextLevelReferrals, NextLevelReferrals
from users.models import User
from unittest.mock import Mock
from referrals.user_referrals import UserReferrals


@pytest.fixture
def create_user_referral():
    def cur():
        user = User.objects.get(pk=1)
        first = DefaultNextLevelReferrals([user.referral_id])
        second = DefaultNextLevelReferrals(list(first.all().referred_id))
        return UserReferrals(first, second)
    return cur


def test_user_referrals():
    assert UserReferrals(Mock(spec=NextLevelReferrals), Mock(spec=NextLevelReferrals))


@pytest.mark.django_db
def test_user_referrals_to_dict(set_fixtures_referrals_case_1, expected_user_referrals, create_user_referral):
    set_fixtures_referrals_case_1()

    assert create_user_referral().to_dict() == expected_user_referrals


@pytest.mark.django_db
def test_user_referrals_to_dict_zero(
        set_fixtures_referrals_case_zero,
        expected_user_zero_referrals,
        create_user_referral
):
    set_fixtures_referrals_case_zero()

    assert create_user_referral().to_dict() == expected_user_zero_referrals


@pytest.mark.django_db
def test_user_referrals_to_dict_zero_second_level(
        set_fixtures_referrals_case_zero_second_level,
        expected_user_referrals_zero_second_level,
        create_user_referral
):
    set_fixtures_referrals_case_zero_second_level()

    assert create_user_referral().to_dict() == expected_user_referrals_zero_second_level


@pytest.mark.django_db
def test_user_referrals_to_dict_case_2(
        set_fixtures_referrals_case_2,
        expected_user_referrals_case_2,
        create_user_referral
):
    set_fixtures_referrals_case_2()

    assert create_user_referral().to_dict() == expected_user_referrals_case_2
