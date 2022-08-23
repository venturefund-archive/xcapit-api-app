import pytest
from django.shortcuts import reverse


@pytest.mark.django_db
def test_investor_test_view_with_default_language(client, create_survey, expected_spanish_survey):
    response = client.get(reverse('surveys:investor-test'))

    assert response.status_code == 200
    assert response.json() == expected_spanish_survey


@pytest.mark.django_db
def test_investor_test_view_with_english_language(client, create_survey, expected_english_survey):
    response = client.get(reverse('surveys:investor-test'), {'language': 'en'})

    assert response.status_code == 200
    assert response.json() == expected_english_survey
