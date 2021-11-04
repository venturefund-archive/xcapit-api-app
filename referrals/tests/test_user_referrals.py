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
