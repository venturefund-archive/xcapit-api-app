import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_investor_category_from_profile(client, test_user):
    url = reverse('profiles:retrieve-update-user-profile', kwargs={'user_id': test_user.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()['investor_category'] == 'wealth_managements.profiles.no_category'
