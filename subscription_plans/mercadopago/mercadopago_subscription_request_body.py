import json
from users.models import User
from subscription_plans.models import PlanModel


class MercadopagoSubscriptionRequestBody:
    def __init__(self, plan: PlanModel, user: User):
        self._user = user
        self._plan = plan

    def json(self):
        return json.dumps({
            'auto_recurring': {
                'currency_id': 'ARS',
                'transaction_amount': self._plan.price,
                'frequency': self._plan.frequency,
                'frequency_type': self._plan.frequency_type
            },
            'back_url': 'https://xcapit.com',
            'external_reference': str(self._user.id),
            'reason': self._plan.name,
            'status': 'pending',
            'payer_email': self._user.email
        })
