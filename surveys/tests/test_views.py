import pytest
from django.shortcuts import reverse


@pytest.mark.django_db
def test_investor_test_view(client, create_survey, expected_json_survey):
    response = client.get(reverse('surveys:investor-test'))

    assert response.status_code == 200
    assert response.json() == expected_json_survey
