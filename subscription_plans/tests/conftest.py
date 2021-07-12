import pytest
from subscription_plans.models import PlanModel
from users import test_utils


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
