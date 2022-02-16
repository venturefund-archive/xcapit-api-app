import pytest
from unittest.mock import Mock
from core.datetime.datetime_of import DefaultDatetimeOf
from core.datetime.datetime_range import DatetimeRange
from referrals.filtered_referral_count import FilteredReferralCount
from referrals.next_level_referrals import DefaultNextLevelReferrals
from referrals.referral_count_of import ReferralCountOf
from users.models import User


@pytest.fixture
def next_level_referrals(set_fixtures_referrals_case_1):
    set_fixtures_referrals_case_1()
    return DefaultNextLevelReferrals(list(User.objects.filter(id=1).values_list('referral_id', flat=True)))


def test_new():
    assert FilteredReferralCount(referral_count=Mock(spec=ReferralCountOf))
    assert FilteredReferralCount(referral_count=Mock(spec=ReferralCountOf), a_datetime_range=DatetimeRange())


@pytest.mark.django_db
def test_value_with_wallet_without_filter(next_level_referrals):
    referral_count = ReferralCountOf(next_level_referrals, True)
    filtered_referral_count = FilteredReferralCount(referral_count)

    assert filtered_referral_count.value() == referral_count.value()


@pytest.mark.django_db
def test_value_with_wallet_since_filter(next_level_referrals):
    referral_count = FilteredReferralCount(
        ReferralCountOf(next_level_referrals, True),
        DatetimeRange(since=DefaultDatetimeOf('2021-04-03T21:30:00.00Z')))

    assert referral_count.value() == 2


@pytest.mark.django_db
def test_value_with_wallet_to_filter(next_level_referrals):
    referral_count = FilteredReferralCount(
        ReferralCountOf(next_level_referrals, True),
        DatetimeRange(to=DefaultDatetimeOf('2021-04-03T21:30:00.00Z')))

    assert referral_count.value() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('since, to, expected_result', [
    [DefaultDatetimeOf('2021-04-05T21:30:00.00Z'), DefaultDatetimeOf('2021-04-06T21:30:00.00Z'), 0],
    [DefaultDatetimeOf('2021-04-02T21:30:00.00Z'), DefaultDatetimeOf('2021-04-03T21:30:00.00Z'), 0],
    [DefaultDatetimeOf('2021-04-03T21:30:00.00Z'), DefaultDatetimeOf('2021-04-05T21:30:00.00Z'), 2]
])
def test_value_with_wallet_since_to_filter(next_level_referrals, since, to, expected_result):
    referral_count = FilteredReferralCount(
        ReferralCountOf(next_level_referrals, True),
        DatetimeRange(since=since, to=to))

    assert referral_count.value() == expected_result
