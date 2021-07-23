import pytest
from unittest.mock import Mock
from subscription_plans.http_methods import FakePostMethod
from subscription_plans.mercadopago.mercadopago_subscription_request_body import MercadopagoSubscriptionRequestBody
from subscription_plans.mercadopago.mercadopago_subscription_request import MercadopagoSubscriptionRequest


def test_mercadopago_subscription_request():
    assert MercadopagoSubscriptionRequest.create(
        FakePostMethod(),
        Mock(spec=MercadopagoSubscriptionRequestBody)
    )


@pytest.mark.django_db
def test_mercadopago_subscription_request_success(mercadopago_subscription_request_body):
    sr = MercadopagoSubscriptionRequest.create(FakePostMethod(), mercadopago_subscription_request_body)
    assert sr.response().status_code == 200
    assert sr.response().json() == {}


@pytest.mark.django_db
def test_mercadopago_subscription_request_error(mercadopago_subscription_request_body):
    sr = MercadopagoSubscriptionRequest.create(
        FakePostMethod(status_code=400, json_res={'error': 'A sad error message'}),
        mercadopago_subscription_request_body
    )
    assert sr.response().status_code == 400
    assert sr.response().json() == {'error': 'A sad error message'}



