from unittest.mock import Mock
from subscription_plans.payer_email import PayerEmail
from subscription_plans.mercadopago.mercadopago_subscription_request_params import MercadopagoSubscriptionRequestParams


def test_subscription_request_params():
    assert MercadopagoSubscriptionRequestParams(Mock(spec=PayerEmail), status='authorized')


def test_subscription_request_params_value():
    params = MercadopagoSubscriptionRequestParams(
        Mock(
            spec=PayerEmail,
            value=lambda: 'test@xcapit.com'
        ),
        status='authorized')
    assert params.value() == {'payer_email': 'test@xcapit.com', 'status': 'authorized'}
