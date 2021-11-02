import pytest
from django.urls import reverse


# @pytest.mark.wip
# @pytest.mark.django_db
# def test_get_user_referrals_count(client, set_fixtures_referrals_case_1):
#     set_fixtures_referrals_case_1()
#     response = client.get(reverse('referrals:get-user-referrals-count', kwargs={'user_id': '1'}))
#     assert response.status_code == 200
#     assert response.json() == {}
