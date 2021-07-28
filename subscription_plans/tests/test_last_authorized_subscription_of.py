import pytest
from unittest.mock import Mock
from core.http.http_methods import FakeHTTPMethod
from subscription_plans.payer_email import PayerEmail
from core.http.empty_request_body import EmptyRequestBody
from subscription_plans.models import PlanSubscriptionModel
from subscription_plans.last_authorized_subscription_of import LastAuthorizedSubscriptionOf
from subscription_plans.mercadopago.mercadopago_payment_request import MercadopagoPaymentRequest
from subscription_plans.mercadopago.mercadopago_subscription_request import MercadopagoSubscriptionRequest


@pytest.mark.wip
def test_subscription_of():
    assert LastAuthorizedSubscriptionOf(Mock())


@pytest.mark.wip
def test_last_authorized_subscription_of(
        mercadopago_subscription_request_search,
        mercadopago_subscription_search_results
):
    subscription = LastAuthorizedSubscriptionOf(
        mercadopago_subscription_request_search(mercadopago_subscription_search_results)
    )
    assert subscription.value() == [{
        'id': 'test_id_1',
        'status': 'authorized',
        'payer_email': 'test@xcapit.com',
        'date_created': '2021-07-21T14:09:48.909-04:00',
        'external_reference': '1'
    }]


@pytest.mark.wip
@pytest.mark.django_db
def test_last_authorized_subscription_of_empty(create_plan_subscription, mercadopago_subscription_request_search):
    create_plan_subscription()
    subscription = LastAuthorizedSubscriptionOf(mercadopago_subscription_request_search([]))
    assert subscription.value() == {}
    subscription.authorize()


@pytest.mark.wip
@pytest.mark.django_db
def test_last_authorized_subscription_of_empty(
        create_plan_subscription,
        mercadopago_subscription_request_search,
        mercadopago_subscription_search_results
):
    create_plan_subscription()
    subscription = LastAuthorizedSubscriptionOf(
        Mock(
            spec=MercadopagoSubscriptionRequest,
            response=lambda: Mock(json=lambda: {'results': mercadopago_subscription_search_results})
        )
    )
    assert PlanSubscriptionModel.objects.get(pk=1).status == 'pending'
    subscription.authorize()
    assert PlanSubscriptionModel.objects.get(pk=1).status == 'authorized'
    assert PlanSubscriptionModel.objects.count() == 1
