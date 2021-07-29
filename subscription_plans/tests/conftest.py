import json
import pytest
from users import test_utils
from datetime import datetime
from core.http.http_methods import FakeHTTPMethod
from core.http.empty_request_body import EmptyRequestBody
from subscription_plans.mercadopago.mercadopago_url import MercadopagoURL
from subscription_plans.mercadopago.mercadopago_headers import DefaultMercadopagoHeaders
from subscription_plans.models import PlanModel, PlanSubscriptionModel, PaymentMethodModel
from subscription_plans.tests.test_mercadopago_subscription_request import DefaultRequestParams
from subscription_plans.mercadopago.mercadopago_subscription_request import MercadopagoSubscriptionRequest
from subscription_plans.tests.test_mercadopago_subscription_request_body import MercadopagoSubscriptionRequestBody


@pytest.fixture
def create_user():
    def cu(email='test@xcapit.com', password='1234Qwerty', is_superuser=False):
        return test_utils.create_user(email, password, is_superuser)

    return cu


@pytest.fixture
def plan_to_save():
    return {
        'name': 'test',
        'info': 'an info',
        'price': '10',
        'type': 'free',
        'state': 'payment.licenses.annual',
        'frequency': 1,
        'frequency_type': 'months',
    }


@pytest.fixture
def plan_saved(plan_to_save):
    plan = PlanModel(**plan_to_save)
    plan.save()
    return plan


@pytest.fixture
def payment_to_save():
    return {
        'amount': 20.3,
        'currency': 'ARS'
    }


@pytest.fixture
def create_payment_method(payment_method_to_save):
    def cpm():
        payment_method = PaymentMethodModel(**payment_method_to_save)
        payment_method.save()
        return payment_method

    return cpm


@pytest.fixture
def create_plan_subscription(create_user, create_payment_method, plan_saved):
    def cps():
        plan_subscription = PlanSubscriptionModel(
            user=create_user(),
            payment_method=create_payment_method(),
            plan=plan_saved,
            start_date=datetime(2020, 10, 1),
            end_date=datetime(2021, 10, 1),
            currency='ARS',
            status='pending'
        )
        plan_subscription.save()
        return plan_subscription

    return cps


@pytest.fixture
def payment_method_to_save():
    return {
        'name': 'Mercadopago',
        'description': 'payment.methods.arg',
        'payment_link': 'test',
        'provider_plan_id': 'asdfasdkfjker9h8'
    }


@pytest.fixture
def mercadopago_json_body():
    return json.dumps({
        'auto_recurring': {
            'currency_id': 'ARS',
            'transaction_amount': '10',
            'frequency': 1,
            'frequency_type': 'months'
        },
        'back_url': 'https://xcapit.com',
        'external_reference': '1',
        'reason': 'test',
        'status': 'pending',
        'payer_email': 'test@xcapit.com'
    })


@pytest.fixture
def mercadopago_subscription_request_body(create_plan_subscription):
    return MercadopagoSubscriptionRequestBody(create_plan_subscription())


@pytest.fixture
def mercadopago_subscription_search_results():
    return [
        {
            'id': 'test_id_1',
            'status': 'authorized',
            'payer_email': 'test@xcapit.com',
            'date_created': '2021-07-21T14:09:48.909-04:00',
            'external_reference': '1'
        },
        {
            'id': 'test_id_2',
            'status': 'pending',
            'payer_email': 'test@xcapit.com',
            'date_created': '2021-07-19T14:09:48.909-04:00',
            'external_reference': '2'
        }
    ]


@pytest.fixture
def mercadopago_subscription_request_search():
    def mrs(results):
        fake_http = FakeHTTPMethod(200, {'total': len(results), 'results': results})
        return MercadopagoSubscriptionRequest(
            fake_http,
            MercadopagoURL('preapproval/search'),
            EmptyRequestBody(),
            DefaultRequestParams({'payer_email': 'test@xcapit.com', 'status': 'authorized'}),
            DefaultMercadopagoHeaders()
        )

    return mrs


@pytest.fixture
def last_authorized_subscription_raw(mercadopago_subscription_search_results):
    return mercadopago_subscription_search_results[0]


@pytest.fixture
def payment_created_webhook_data():
    return {
        "action": "payment.created",
        "api_version": "v1",
        "data": {
            "id": "16065484941"
        },
        "date_created": "2021-07-27T20:35:08Z",
        "id": 7764932952,
        "live_mode": True,
        "type": "payment",
        "user_id": "141910043"
    }