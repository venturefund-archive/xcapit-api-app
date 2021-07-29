import pytest
from subscription_plans.mercadopago.mercadopago_subscription_request_body import MercadopagoSubscriptionRequestBody


@pytest.mark.django_db
def test_mercadopago_subscription_request_body(create_plan_subscription):
    assert MercadopagoSubscriptionRequestBody(create_plan_subscription())


@pytest.mark.django_db
def test_mercadopago_subscription_request_body_json(create_plan_subscription, mercadopago_json_body):
    assert MercadopagoSubscriptionRequestBody(create_plan_subscription()).json() == mercadopago_json_body
