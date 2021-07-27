import json
from core.http.request_body import RequestBody
from subscription_plans.models import PlanSubscriptionModel


class MercadopagoSubscriptionRequestBody(RequestBody):
    def __init__(self, plan_subscription: PlanSubscriptionModel):
        self._plan_subscription = plan_subscription

    def json(self):
        return json.dumps({
            'auto_recurring': {
                'currency_id': 'ARS',
                'transaction_amount': self._plan_subscription.plan.price,
                'frequency': self._plan_subscription.plan.frequency,
                'frequency_type': self._plan_subscription.plan.frequency_type
            },
            'back_url': 'https://xcapit.com',
            'external_reference': str(self._plan_subscription.pk),
            'reason': self._plan_subscription.plan.name,
            'status': 'pending',
            'payer_email': self._plan_subscription.user.email
        })
