import json
import pytest
from subscription_plans.mercadopago.mercadopago_payment_request_body import MercadopagoPaymentRequestBody


@pytest.mark.wip
def test_mercadopago_payment_request_body():
    assert MercadopagoPaymentRequestBody({})


@pytest.mark.wip
def test_mercadopago_payment_request_body_json():
    assert MercadopagoPaymentRequestBody({}).json() == json.dumps({})

