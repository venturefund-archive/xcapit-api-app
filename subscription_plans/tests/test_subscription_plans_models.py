import pytest
from subscription_plans.models import PlanSubscriptionModel


@pytest.mark.django_db
def test_plan_subscription_model(create_user):
    model = PlanSubscriptionModel(user=create_user())

    model.save()

    assert len(PlanSubscriptionModel.objects.all()) == 1
