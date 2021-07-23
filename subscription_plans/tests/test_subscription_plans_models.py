import pytest
from datetime import datetime
from subscription_plans.models import PlanSubscriptionModel, PlanModel, PaymentMethodModel, PaymentModel


@pytest.mark.django_db
def test_plan_subscription_model(create_user, create_payment_method, plan_saved):
    model = PlanSubscriptionModel(
        user=create_user(),
        payment_method=create_payment_method(),
        plan=plan_saved,
        start_date=datetime(2020, 10, 1),
        end_date=datetime(2021, 10, 1),
        currency='ARS'
    )

    model.save()

    assert len(PlanSubscriptionModel.objects.all()) == 1


@pytest.mark.django_db
def test_plan_model(plan_to_save):
    model = PlanModel(**plan_to_save)

    model.save()

    assert len(PlanModel.objects.all()) == 1


@pytest.mark.django_db
def test_payment_method_model(payment_method_to_save):
    model = PaymentMethodModel(**payment_method_to_save)

    model.save()

    assert len(PaymentMethodModel.objects.all()) == 1


@pytest.mark.django_db
def test_payment_model(payment_to_save, create_plan_subscription):
    model = PaymentModel(
        plan_subscription=create_plan_subscription(),
        **payment_to_save
    )

    model.save()

    assert len(PaymentModel.objects.all()) == 1
    assert model.plan_subscription.id == 1
