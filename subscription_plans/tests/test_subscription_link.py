from requests import Response
from unittest.mock import Mock
from subscription_plans.subscription_link import SubscriptionLink


def test_subscription_link():
    assert SubscriptionLink(Mock(spec=Response))


def test_subscription_link_value():
    subscription_link = SubscriptionLink(Mock(spec=Response, json=lambda: {'init_point': 'test_subscription_link'}))
    assert subscription_link.value() == 'test_subscription_link'
