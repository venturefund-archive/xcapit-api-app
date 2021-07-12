import pytest
from subscription_plans.models import PlanSubscriptionModel, PlanModel


@pytest.mark.django_db
def test_plan_subscription_model(create_user, plan_saved):
    model = PlanSubscriptionModel(user=create_user(), plan=plan_saved)

    model.save()

    assert len(PlanSubscriptionModel.objects.all()) == 1


@pytest.mark.django_db
def test_plan_model(plan_to_save):
    model = PlanModel(**plan_to_save)

    model.save()

    assert len(PlanModel.objects.all()) == 1
