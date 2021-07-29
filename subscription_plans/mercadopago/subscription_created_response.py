from requests import Response
from subscription_plans.subscription_link import SubscriptionLink


class SubscriptionCreatedResponse:
    def __init__(self, response: Response):
        self._response = response

    def link(self) -> SubscriptionLink:
        return SubscriptionLink(self._response)
