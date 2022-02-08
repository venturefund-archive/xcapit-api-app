import pandas
import pytest
from users.models import User
from unittest.mock import Mock
from referrals.referral_count_of import ReferralCountOf
from referrals.next_level_referrals import NextLevelReferrals


def test_referral_count_of():
    assert ReferralCountOf(Mock(), Mock())


@pytest.mark.django_db
def test_referral_count_of_value_with_wallet(set_fixtures_referrals_case_1):
    set_fixtures_referrals_case_1()

    referrals = NextLevelReferrals(list(User.objects.filter(id=1).values_list('referral_id', flat=True)))
    referral_count = ReferralCountOf(referrals, True)

    assert referral_count.value() == 2


@pytest.mark.django_db
def test_referral_count_of_value_without_wallet(set_fixtures_referrals_case_1):
    set_fixtures_referrals_case_1()

    first_level = NextLevelReferrals(list(User.objects.filter(id=1).values_list('referral_id', flat=True)))
    referrals = NextLevelReferrals(list(first_level.all().referred_id))

    assert ReferralCountOf(referrals, False).value() == 3


@pytest.mark.django_db
def test_referral_count_of_value_with_wallet_case_2(set_fixtures_referrals_case_2):
    set_fixtures_referrals_case_2()

    first_level = NextLevelReferrals(list(User.objects.filter(id=1).values_list('referral_id', flat=True)))
    second_level = NextLevelReferrals(list(first_level.all().referred_id))

    assert ReferralCountOf(first_level, True).value() == 1
    assert ReferralCountOf(second_level, True).value() == 0
    assert ReferralCountOf(first_level, False).value() == 0
    assert ReferralCountOf(second_level, False).value() == 0


@pytest.mark.django_db
def test_referral_count_of_raw_df(set_fixtures_referrals_case_1):
    set_fixtures_referrals_case_1()

    referrals = NextLevelReferrals(list(User.objects.filter(id=1).values_list('referral_id', flat=True)))
    referral_count = ReferralCountOf(referrals, True)

    assert isinstance(referral_count.raw_df(), pandas.DataFrame)
