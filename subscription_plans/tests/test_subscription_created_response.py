import pytest
from requests import Response
from unittest.mock import Mock
from subscription_plans.mercadopago.subscription_created_response import SubscriptionCreatedResponse


def test_subscription_created_response():
    assert SubscriptionCreatedResponse(Mock(spec=Response))


@pytest.mark.django_db
def test_subscription_created_response_link():
    subscription_response = SubscriptionCreatedResponse(
        Mock(
            spec=Response,
            json=lambda: {'init_point': 'test_subscription_link', 'date_created': '2021-07-19T14:09:48.909-04:00'}
        )
    )
    assert subscription_response.link()
    assert subscription_response.link().value() == 'test_subscription_link'
