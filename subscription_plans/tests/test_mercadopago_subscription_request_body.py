# Le pegamos al endpoint con id de usuario y plan.
# Creo la subscription en mercadopago.
# Creo la subscription en nuestro sistema en estado pendiente.
# Retorno el link de pago de la subscripcion.



# SubscriptionLink(....)
# responsabilidades:
# brindar el link como un string
# colaboradores:
# MercadopagoSubscriptionRequest

# MercadopagoSubscriptionRequest ✅
# colaboradores:
# BodyMercadopago

# BodyMercadopago ✅
# responsabilidades:
# brindar el dict value para enviar a mercadopago
# colaboradores:
# PlanModel, User

import pytest
from subscription_plans.mercadopago.mercadopago_subscription_request_body import MercadopagoSubscriptionRequestBody


@pytest.mark.django_db
def test_mercadopago_subscription_request_body(plan_saved, create_user):
    assert MercadopagoSubscriptionRequestBody(plan_saved, create_user())


@pytest.mark.django_db
def test_mercadopago_subscription_request_body_json(plan_saved, create_user, mercadopago_json_body):
    assert MercadopagoSubscriptionRequestBody(plan_saved, create_user('test@test.com')).json() == mercadopago_json_body
