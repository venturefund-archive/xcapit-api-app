import json
from subscription_plans.mercadopago.mercadopago_payment_request_body import MercadopagoPaymentRequestBody


def test_mercadopago_payment_request_body():
    assert MercadopagoPaymentRequestBody({})


def test_mercadopago_payment_request_body_json():
    assert MercadopagoPaymentRequestBody({}).json() == json.dumps({})

