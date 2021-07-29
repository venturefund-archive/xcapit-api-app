from core.http.http_methods import PostMethod
from subscription_plans.models import PlanSubscriptionModel
from subscription_plans.mercadopago.subscription_created_response import SubscriptionCreatedResponse
from subscription_plans.mercadopago.mercadopago_subscription_request import MercadopagoSubscriptionRequest
from subscription_plans.mercadopago.mercadopago_subscription_request_body import MercadopagoSubscriptionRequestBody


class Subscription:
    def __init__(
            self,
            plan_subscription: PlanSubscriptionModel,
            mercadopago_subscription_request: MercadopagoSubscriptionRequest
    ):
        self._mercadopago_subscription_request = mercadopago_subscription_request
        self._plan_subscription = plan_subscription

    @classmethod
    def create(cls, plan_subscription: PlanSubscriptionModel):
        return cls(
            plan_subscription,
            MercadopagoSubscriptionRequest.create(
                PostMethod(),
                MercadopagoSubscriptionRequestBody(plan_subscription)
            )
        )

    def created(self):
        return SubscriptionCreatedResponse(self._mercadopago_subscription_request.response())
