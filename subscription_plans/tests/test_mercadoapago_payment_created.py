from unittest.mock import Mock
from subscription_plans.mercadopago.payment_created_event import PaymentCreatedEvent


def test_payment_created_event():
    assert PaymentCreatedEvent({}, Mock())


def test_payment_created_event_create():
    assert PaymentCreatedEvent.create({'data': {'id': '1'}})


def test_payment_created_event_dispatch():
    mock_last_authorized_subscription = Mock()
    PaymentCreatedEvent({}, mock_last_authorized_subscription).dispatch()
    mock_last_authorized_subscription.authorize.assert_called()
    mock_last_authorized_subscription.remove_pending.assert_called()
