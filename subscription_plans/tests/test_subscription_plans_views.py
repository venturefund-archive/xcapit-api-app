import pytest
from django.urls import reverse
from subscription_plans.models import PlanSubscriptionModel
from rest_framework import status


def test_get_payment_methods_returns_an_emtpy_array(client):
    response = client.get(reverse('subscription_plans:payment_methods_by_plan', kwargs={'plan_id': 1}))

    assert response.json() == []


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
