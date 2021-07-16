import pytest
from datetime import datetime
from users import test_utils
from subscription_plans.models import PlanModel, PlanSubscriptionModel, PaymentMethodModel


@pytest.fixture
def create_user():
    def cu(email='maxi@maxi.com', password='1234Qwerty', is_superuser=False):
        return test_utils.create_user(email, password, is_superuser)

    return cu


@pytest.fixture
def plan_to_save():
    return {
        'name': 'test',
        'info': 'an info',
        'price': '',
        'type': 'free',
        'state': 'payment.licenses.annual'
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
            frequency=1,
            frequency_type='months',
            currency='ARS'
        )
        plan_subscription.save()
        return plan_subscription

    return cps


@pytest.fixture
def payment_method_to_save():
    return {
        'name': 'Mercadopago',
        'description': 'payment.methods.arg'
    }
