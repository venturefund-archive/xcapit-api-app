import pytest
from django.shortcuts import reverse


@pytest.mark.django_db
def test_investor_test_view_with_default_language_when_language_is_not_send(client, create_survey,
                                                                            expected_english_survey):
    response = client.get(reverse('surveys:investor-test'))

    assert response.status_code == 200
    assert response.json() == expected_english_survey


@pytest.mark.django_db
def test_investor_test_view_with_english_language(client, create_survey, expected_english_survey):
    response = client.get(reverse('surveys:investor-test'), data={'language': 'en'})

    assert response.status_code == 200
    assert response.json() == expected_english_survey


@pytest.mark.django_db
def test_investor_test_view_with_default_language_when_language_is_not_available(client, create_survey,
                                                                                 expected_english_survey):
    response = client.get(reverse('surveys:investor-test'), data={'language': 'fr'})

    assert response.status_code == 200
    assert response.json() == expected_english_survey
