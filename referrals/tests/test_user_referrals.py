import pytest
from users.models import User
from unittest.mock import Mock
from referrals.user_referrals import UserReferrals


def test_user_referrals():
    assert UserReferrals(Mock())


@pytest.mark.django_db
def test_user_referrals_to_dict(set_fixtures_referrals_case_1, expected_user_referrals):
    set_fixtures_referrals_case_1()
    assert UserReferrals(User.objects.get(pk=1)).to_dict() == expected_user_referrals


@pytest.mark.django_db
def test_user_referrals_to_dict_zero(set_fixtures_referrals_case_zero, expected_user_zero_referrals):
    set_fixtures_referrals_case_zero()
    assert UserReferrals(User.objects.get(pk=1)).to_dict() == expected_user_zero_referrals


@pytest.mark.django_db
def test_user_referrals_to_dict_zero_second_level(
        set_fixtures_referrals_case_zero_second_level,
        expected_user_referrals_zero_second_level
):
    set_fixtures_referrals_case_zero_second_level()
    assert UserReferrals(User.objects.get(pk=1)).to_dict() == expected_user_referrals_zero_second_level


@pytest.mark.django_db
def test_user_referrals_to_dict_case_2(set_fixtures_referrals_case_2, expected_user_referrals_case_2):
    set_fixtures_referrals_case_2()
    assert UserReferrals(User.objects.get(pk=1)).to_dict() == expected_user_referrals_case_2
