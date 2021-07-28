import pytest
from unittest.mock import Mock
from subscription_plans.webhook_event import FakeWebhookEvent
from subscription_plans.mercadopago.mercadopago_webhook import MercadopagoWebhook


@pytest.mark.wip
def test_mercadopago_webhook():
    assert MercadopagoWebhook(Mock(), Mock())


@pytest.mark.wip
def test_mercadopago_webhook_action(payment_created_webhook_data):
    mercadopago_webhook = MercadopagoWebhook(payment_created_webhook_data, {})
    assert mercadopago_webhook.action == 'payment.created'


@pytest.mark.wip
def test_mercadopago_webhook_action_event(payment_created_webhook_data):
    mercadopago_webhook = MercadopagoWebhook(
        payment_created_webhook_data,
        {'payment.created': FakeWebhookEvent}
    )
    mercadopago_webhook.dispatch_events()
    assert True

