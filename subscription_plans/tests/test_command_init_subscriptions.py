import pytest
from io import StringIO
from django.core.management import call_command
from subscription_plans.models import PlanModel


@pytest.mark.wip
@pytest.mark.django_db
def test_command_init_subscription():
    out = StringIO()
    call_command('init_subscriptions', *['--paid_plan_price', '10'], stdout=out)
    assert 'Success' in out.getvalue()
    assert PlanModel.objects.filter(type='free').count() == 1
    paid_plans = PlanModel.objects.filter(type='paid')
    assert paid_plans.count() == 1
    assert paid_plans.first().price == '10'
