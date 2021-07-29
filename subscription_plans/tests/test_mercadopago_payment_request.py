from core.http.http_methods import FakeHTTPMethod
from subscription_plans.mercadopago.mercadopago_payment_request import MercadopagoPaymentRequest
from subscription_plans.mercadopago.mercadopago_payment_request_body import MercadopagoPaymentRequestBody


def test_mercadopago_payment_request():
    assert MercadopagoPaymentRequest.create(FakeHTTPMethod(), 1, MercadopagoPaymentRequestBody({}))


def test_mercadopago_payment_request_response():
    request = MercadopagoPaymentRequest.create(FakeHTTPMethod(), 1, MercadopagoPaymentRequestBody({}))
    assert request.response().json() == {}
    assert request.response().status_code == 200


def test_mercadopago_payment_request_response_error():
    request = MercadopagoPaymentRequest.create(
        FakeHTTPMethod(400, {'error': 'A sad error message'}),
        1,
        MercadopagoPaymentRequestBody({})
    )
    assert request.response().json() == {'error': 'A sad error message'}
    assert request.response().status_code == 400
