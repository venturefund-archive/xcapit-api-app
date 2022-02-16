import pytest
from referrals.tests.conftest import create_with_utc
from referrals.next_level_referrals import DefaultNextLevelReferrals, NextLevelReferrals, FakeNextLevelReferrals
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


@pytest.fixture
def create_user_referral_with_fakes():
    def cur(first, second):
        first = FakeNextLevelReferrals(create_with_utc(first))
        second = FakeNextLevelReferrals(create_with_utc(second))
        return UserReferrals(first, second)
    return cur


def test_user_referrals():
    assert UserReferrals(Mock(spec=NextLevelReferrals), Mock(spec=NextLevelReferrals))


def test_user_referrals_to_dict(
        expected_user_referrals,
        expected_first_level,
        expected_second_level,
        create_user_referral_with_fakes
):
    user_referrals = create_user_referral_with_fakes(expected_first_level, expected_second_level)

    assert user_referrals.to_dict() == expected_user_referrals


@pytest.mark.django_db
def test_user_referrals_to_dict_zero(
        set_fixtures_referrals_case_zero,
        expected_user_zero_referrals,
        create_user_referral
):
    set_fixtures_referrals_case_zero()

    assert create_user_referral().to_dict() == expected_user_zero_referrals


def test_user_referrals_to_dict_zero_second_level(
        empty_next_level,
        expected_referrals_case_zero_second_level,
        expected_user_referrals_zero_second_level,
        create_user_referral_with_fakes
):
    user_referrals = create_user_referral_with_fakes(expected_referrals_case_zero_second_level, empty_next_level)

    assert user_referrals.to_dict() == expected_user_referrals_zero_second_level


def test_user_referrals_to_dict_case_2(
        empty_next_level,
        expected_referrals_case_case_2_level_one,
        expected_user_referrals_case_2,
        create_user_referral_with_fakes
):
    user_referrals = create_user_referral_with_fakes(expected_referrals_case_case_2_level_one, empty_next_level)

    assert user_referrals.to_dict() == expected_user_referrals_case_2
