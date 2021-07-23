import pytest
from subscription_plans.mercadopago.mercadopago_url import MercadopagoURL


def test_mercadopago_url():
    mp_url = MercadopagoURL('test', 'some_')
    assert str(mp_url) == 'some_test'
    assert f'{mp_url}' == 'some_test'
