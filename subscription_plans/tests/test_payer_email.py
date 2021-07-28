import pytest
from requests import Response
from unittest.mock import Mock
from subscription_plans.payer_email import PayerEmail
from subscription_plans.mercadopago.mercadopago_payment_request import MercadopagoPaymentRequest


@pytest.mark.wip
def test_payer_email():
    assert PayerEmail(Mock(spec=MercadopagoPaymentRequest))


@pytest.mark.wip
def test_payer_email_value():
    payer_email = PayerEmail(
        Mock(
            spec=MercadopagoPaymentRequest,
            response=lambda: Mock(spec=Response, json=lambda: {'payer': {'email': 'test@xcapit.com'}})
        )
    )
    assert payer_email.value() == 'test@xcapit.com'
