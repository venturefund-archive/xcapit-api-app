import pytest
from profiles.models import Profile
from unittest.mock import Mock
from surveys.user_investor_category import UserInvestorCategory


def test_user_investor_category():
    assert UserInvestorCategory(Mock(spec=Profile))


@pytest.mark.django_db
@pytest.mark.parametrize('user_score, expected_category', [
    [0, 'wealth_managements.profiles.no_category'],
    [1, 'wealth_managements.profiles.conservative'],
    [5, 'wealth_managements.profiles.conservative'],
    [7, 'wealth_managements.profiles.conservative'],
    [8, 'wealth_managements.profiles.medium'],
    [13, 'wealth_managements.profiles.medium'],
    [14, 'wealth_managements.profiles.risky'],
    [18, 'wealth_managements.profiles.risky'],
    [19, 'wealth_managements.profiles.no_category']
])
def test_user_investor_category_value(create_categories, user_profile_with_investor_score, user_score,
                                      expected_category):
    profile = user_profile_with_investor_score(user_score)
    assert UserInvestorCategory(profile).value() == expected_category
