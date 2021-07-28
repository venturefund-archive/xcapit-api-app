import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import Mock, patch
from subscription_plans.models import PlanSubscriptionModel


def test_get_payment_methods_returns_an_emtpy_array(client):
    response = client.get(reverse('subscription_plans:payment_methods_by_plan', kwargs={'plan_id': 1}))

    assert response.json() == []


@pytest.mark.django_db
def test_create_a_free_subscription_view(client, create_user, plan_saved):
    data = {'user_id': create_user().pk}

    response = client.post(reverse('subscription_plans:create_free_subscription'), data=data)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_a_free_subscription_saves_on_db(client, create_user, plan_saved):
    data = {'user_id': create_user().pk}

    client.post(reverse('subscription_plans:create_free_subscription'), data=data)

    assert len(PlanSubscriptionModel.objects.all()) == 1


@pytest.mark.wip
@pytest.mark.django_db
@patch('requests.Session.post')
def test_paid_subscription_link_view(mock_post, client, create_user, plan_saved, create_payment_method):
    mock_post.return_value = Mock(json=lambda: {'init_point': 'test_link'}, status_code=201)
    user = create_user('test@xcapit.com')
    data = {
        'user_id': user.id,
        'plan_id': plan_saved.id,
        'payment_method_id': create_payment_method().id
    }
    response = client.post(reverse('subscription_plans:paid_subscription_link'), data=data)
    assert response.status_code == 200
    assert response.json() == {'link': 'test_link'}


@pytest.mark.wip
@pytest.mark.django_db
@patch('subscription_plans.views.PaymentCreatedEvent')
def test_mercadopago_webhook_view(mock_payment_event, client, payment_created_webhook_data):
    mock_payment_event.create = Mock(dispatch=lambda: None)
    response = client.post(reverse('subscription_plans:mercadopago_webhook'), data=payment_created_webhook_data)
    assert response.status_code == 200
    mock_payment_event.create.return_value.dispatch.assert_called()
