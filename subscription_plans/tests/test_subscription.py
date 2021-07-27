import pytest
from requests import Response
from unittest.mock import Mock, patch
from subscription_plans.subscription import Subscription


@pytest.mark.wip
def test_subscription():
    assert Subscription(Mock(), Mock())


@pytest.mark.wip
@pytest.mark.django_db
def test_subscription_create(create_plan_subscription):
    assert Subscription.create(create_plan_subscription())


@pytest.mark.wip
@pytest.mark.django_db
@patch('requests.Session.post')
def test_subscription_created(mock_post, create_plan_subscription):
    mock_post.return_value = Mock(spec=Response, status_code=201, json=lambda: {})
    subscription = Subscription.create(create_plan_subscription())
    assert subscription.created()
