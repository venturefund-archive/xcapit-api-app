from functools import lru_cache as cache
from subscription_plans.payer_email import PayerEmail
from subscription_plans.models import PlanSubscriptionModel
from subscription_plans.sorted_subscriptions import SortedSubscriptions
from subscription_plans.mercadopago.mercadopago_subscription_request import MercadopagoSubscriptionRequest


class LastAuthorizedSubscriptionOf:
    def __init__(self, payer_email: PayerEmail, subscription_request: MercadopagoSubscriptionRequest):
        self._payer_email = payer_email
        self._subscription_request = subscription_request

    @cache
    def _subscriptions(self) -> list:
        return self._subscription_request.response().json().get('results')

    def value(self):
        return SortedSubscriptions(self._subscriptions(), key=lambda sub: sub.get('date_created')).last()

    def authorize(self):
        PlanSubscriptionModel.objects \
            .filter(id=int(self.value()[0].get('external_reference')), status='pending') \
            .update(status='authorized')

    def remove_pending(self):
        if len(self.value()):
            PlanSubscriptionModel.objects.filter(email=self._payer_email.value(), status='pending').delete()
