from subscription_plans.http_methods import PostMethod
from subscription_plans.mercadopago.mercadopago_subscription_request_body import MercadopagoSubscriptionRequestBody
from subscription_plans.models import PlanModel
from subscription_plans.tests.test_mercadopago_subscription_request import MercadopagoSubscriptionRequest
from users.models import User


class SubscriptionLink:
    def __init__(self, subscription_request: MercadopagoSubscriptionRequest):
        self._subscription_request = subscription_request

    @classmethod
    def create(cls, plan: PlanModel, user: User):
        return cls(
            MercadopagoSubscriptionRequest.create(
                PostMethod(),
                MercadopagoSubscriptionRequestBody(plan, user)
            )
        )

    def value(self):
        return self._subscription_request.response().json().get('init_point')
