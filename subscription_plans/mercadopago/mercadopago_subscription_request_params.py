from core.http.request_params import RequestParams
from subscription_plans.payer_email import PayerEmail


class MercadopagoSubscriptionRequestParams(RequestParams):
    def __init__(self, payer_email: PayerEmail, **kwargs):
        self._payer_email = payer_email
        self._kwargs = kwargs

    def value(self):
        return {'payer_email': self._payer_email.value(), **self._kwargs}
