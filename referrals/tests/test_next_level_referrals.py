# Case 1:
# user (wallets)
#     - for_1 (wallets)
#         - sor_11 (wallets)
#         - sor_12
#         - sor_13 (wallets)
#     - for_2
#     - for_3
#         - sor_31 (wallets)
#         - sor_32
#         - sor_33
#         - sor_34 (not accepted)
#     - for_4 (wallets)


import pytest
import pandas as pd
from users.models import User
from referrals.next_level_referrals import NextLevelReferrals


@pytest.mark.django_db
def test_first_and_second_level_referrals(
        set_fixtures_referrals_case_1,
        expected_first_level,
        expected_second_level
):
    set_fixtures_referrals_case_1()
    first_level = NextLevelReferrals(list(User.objects.filter(id=1).values_list('referral_id', flat=True)))
    second_level = NextLevelReferrals(list(first_level.all().referred_id))

    pd.testing.assert_frame_equal(first_level.all(), expected_first_level)
    pd.testing.assert_frame_equal(second_level.all(), expected_second_level)


@pytest.mark.django_db
def test_zero_referrals(set_fixtures_referrals_case_zero):
    set_fixtures_referrals_case_zero()
    first_level = NextLevelReferrals(list(User.objects.filter(id=1).values_list('referral_id', flat=True)))
    second_level = NextLevelReferrals(list(first_level.all().referred_id))

    assert first_level.all().empty
    assert second_level.all().empty


@pytest.mark.django_db
def test_zero_second_level_referrals(
        set_fixtures_referrals_case_zero_second_level,
        expected_referrals_case_zero_second_level
):
    set_fixtures_referrals_case_zero_second_level()
    first_level = NextLevelReferrals(list(User.objects.filter(id=1).values_list('referral_id', flat=True)))
    second_level = NextLevelReferrals(list(first_level.all().referred_id))

    assert second_level.all().empty
    pd.testing.assert_frame_equal(first_level.all(), expected_referrals_case_zero_second_level)
