import pytest
from unittest.mock import Mock
from core.http.http_methods import FakeHTTPMethod
from core.http.empty_request_body import EmptyRequestBody
from core.http.default_request_params import DefaultRequestParams
from subscription_plans.mercadopago.mercadopago_url import MercadopagoURL
from subscription_plans.mercadopago.mercadopago_headers import DefaultMercadopagoHeaders
from subscription_plans.mercadopago.mercadopago_subscription_request import MercadopagoSubscriptionRequest
from subscription_plans.mercadopago.mercadopago_subscription_request_body import MercadopagoSubscriptionRequestBody


def test_mercadopago_subscription_request():
    assert MercadopagoSubscriptionRequest.create(
        FakeHTTPMethod(),
        Mock(spec=MercadopagoSubscriptionRequestBody)
    )


@pytest.mark.django_db
def test_mercadopago_subscription_request_success(mercadopago_subscription_request_body):
    sr = MercadopagoSubscriptionRequest.create(FakeHTTPMethod(), mercadopago_subscription_request_body)
    assert sr.response().status_code == 200
    assert sr.response().json() == {}


@pytest.mark.django_db
def test_mercadopago_subscription_request_error(mercadopago_subscription_request_body):
    sr = MercadopagoSubscriptionRequest.create(
        FakeHTTPMethod(status_code=400, json_res={'error': 'A sad error message'}),
        mercadopago_subscription_request_body
    )
    assert sr.response().status_code == 400
    assert sr.response().json() == {'error': 'A sad error message'}


@pytest.mark.django_db
def test_mercadopago_subscription_request_search():
    sr = MercadopagoSubscriptionRequest(
        FakeHTTPMethod(),
        MercadopagoURL('preapproval/search'),
        EmptyRequestBody(),
        DefaultRequestParams({'payer_id': '123'}),
        DefaultMercadopagoHeaders()
    )
    assert sr.response().status_code == 200
    assert sr.response().json() == {}
