import pytest
from unittest.mock import patch
from django.urls import reverse


@pytest.mark.django_db
@patch('referrals.views.UserReferrals.to_dict')
def test_get_user_referrals_count(to_dict, client, set_fixtures_referrals_case_1, expected_user_referrals):
    set_fixtures_referrals_case_1()
    to_dict.return_value = expected_user_referrals

    response = client.get(reverse('referrals:get-user-referrals-count', kwargs={'user_id': '1'}))

    assert response.status_code == 200
    assert response.json() == expected_user_referrals


@pytest.mark.django_db
def test_get_user_referrals_count_zero(client, set_fixtures_referrals_case_zero, expected_user_zero_referrals):
    set_fixtures_referrals_case_zero()

    response = client.get(reverse('referrals:get-user-referrals-count', kwargs={'user_id': '1'}))

    assert response.status_code == 200
    assert response.json() == expected_user_zero_referrals


@pytest.mark.django_db
@patch('referrals.views.UserReferrals.to_dict')
def test_get_user_referrals_count_zero_second_level(
        to_dict,
        client,
        set_fixtures_referrals_case_zero_second_level,
        expected_user_referrals_zero_second_level
):
    set_fixtures_referrals_case_zero_second_level()
    to_dict.return_value = expected_user_referrals_zero_second_level

    response = client.get(reverse('referrals:get-user-referrals-count', kwargs={'user_id': '1'}))

    assert response.status_code == 200
    assert response.json() == expected_user_referrals_zero_second_level


@pytest.mark.django_db
def test_get_user_referrals_count_user_not_exists(client):
    response = client.get(reverse('referrals:get-user-referrals-count', kwargs={'user_id': '123123412'}))

    assert response.status_code == 404
    assert response.json() == {'detail': 'Not found.'}
