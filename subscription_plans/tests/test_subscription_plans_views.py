import pytest
from django.urls import reverse
from subscription_plans.models import PlanSubscriptionModel, PaymentMethodModel
from rest_framework import status


@pytest.mark.wip
@pytest.mark.django_db
@pytest.mark.parametrize('plan_id, expected_response', [
    [1, []],
    [2, [{'description': 'payment.methods.arg', 'id': 1, 'name': 'Mercadopago'}]]
])
def test_get_payment_methods_by_plan(client, plan_id, expected_response, create_payment_method):
    create_payment_method()
    response = client.get(reverse('subscription_plans:payment_methods_by_plan', kwargs={'plan_id': plan_id}))
    assert response.json() == expected_response


@pytest.mark.django_db
def test_create_a_free_subscription_view(client, create_user, plan_saved, create_payment_method):
    create_payment_method()
    data = {'user_id': create_user().pk}

    response = client.post(reverse('subscription_plans:create_free_subscription'), data=data)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_a_free_subscription_saves_on_db(client, create_user, plan_saved, create_payment_method):
    create_payment_method()
    data = {'user_id': create_user().pk}

    client.post(reverse('subscription_plans:create_free_subscription'), data=data)

    assert len(PlanSubscriptionModel.objects.all()) == 1
