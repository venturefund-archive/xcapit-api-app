from requests import Response
from subscription_plans.models import PlanSubscriptionModel
from subscription_plans.subscription_link import SubscriptionLink


class SubscriptionCreatedResponse:
    def __init__(self, plan_subscription: PlanSubscriptionModel, response: Response):
        self._plan_subscription = plan_subscription
        self._response = response

    def link(self) -> SubscriptionLink:
        return SubscriptionLink(self._response)
