import pytest
from unittest.mock import Mock, patch
from subscription_plans.subscription_link import SubscriptionLink
from subscription_plans.tests.test_mercadopago_subscription_request import MercadopagoSubscriptionRequest, \
    FakePostMethod


def test_subscription_link():
    assert SubscriptionLink(Mock(spec=MercadopagoSubscriptionRequest))


@pytest.mark.django_db
def test_subscription_link_value(mercadopago_subscription_request_body):
    subscription_link = SubscriptionLink(
        MercadopagoSubscriptionRequest.create(
            FakePostMethod(json_res={'init_point': 'test_subscription_link'}, status_code=201),
            mercadopago_subscription_request_body,
        )
    )
    assert subscription_link.value() == 'test_subscription_link'


@pytest.mark.django_db
@patch('requests.Session.post')
def test_subscription_link_create(mock_post, create_user, plan_saved):
    mock_post.return_value = Mock(json=lambda *args, **kwargs: {'init_point': 'test_subscription_link'}, status_code=201)
    subscription_link = SubscriptionLink.create(plan_saved, create_user())
    assert subscription_link.value() == 'test_subscription_link'
