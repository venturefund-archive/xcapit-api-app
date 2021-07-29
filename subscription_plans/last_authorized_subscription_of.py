from functools import lru_cache as cache
from subscription_plans.models import PlanSubscriptionModel
from subscription_plans.sorted_subscriptions import SortedSubscriptions
from subscription_plans.mercadopago.mercadopago_subscription_request import MercadopagoSubscriptionRequest


class LastAuthorizedSubscriptionOf:
    def __init__(self, subscription_request: MercadopagoSubscriptionRequest):
        self._subscription_request = subscription_request

    def _subscriptions(self) -> list:
        return self._subscription_request.response().json().get('results')

    @cache
    def value(self):
        return SortedSubscriptions(self._subscriptions(), key=lambda sub: sub.get('date_created')).last()

    def authorize(self):
        PlanSubscriptionModel.objects.filter(
            id=int(self.value()[0].get('external_reference'))
        ).update(status='authorized')

    def remove_pending(self):
        if len(self.value()):
            user = PlanSubscriptionModel.objects.filter(
                id=int(self.value()[0].get('external_reference'))
            ).first().user
            PlanSubscriptionModel.objects.filter(user=user, status='pending').delete()
