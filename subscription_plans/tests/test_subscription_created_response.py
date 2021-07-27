import pytest
from requests import Response
from unittest.mock import Mock
from subscription_plans.models import PlanSubscriptionModel
from subscription_plans.mercadopago.subscription_created_response import SubscriptionCreatedResponse


@pytest.mark.wip
def test_subscription_created_response():
    assert SubscriptionCreatedResponse(Mock(spec=PlanSubscriptionModel), Mock(spec=Response))


@pytest.mark.wip
@pytest.mark.django_db
def test_subscription_created_response_link(create_plan_subscription):
    subscription_response = SubscriptionCreatedResponse(
        create_plan_subscription(),
        Mock(
            spec=Response,
            json=lambda: {'init_point': 'test_subscription_link', 'date_created': '2021-07-19T14:09:48.909-04:00'}
        )
    )
    assert subscription_response.link()
    assert subscription_response.link().value() == 'test_subscription_link'
