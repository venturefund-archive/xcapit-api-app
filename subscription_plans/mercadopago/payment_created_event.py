from core.http.http_methods import GetMethod
from subscription_plans.payer_email import PayerEmail
from subscription_plans.webhook_event import WebhookEvent
from core.http.empty_request_body import EmptyRequestBody
from subscription_plans.mercadopago.mercadopago_url import MercadopagoURL
from subscription_plans.mercadopago.mercadopago_headers import DefaultMercadopagoHeaders
from subscription_plans.last_authorized_subscription_of import LastAuthorizedSubscriptionOf
from subscription_plans.mercadopago.mercadopago_payment_request import MercadopagoPaymentRequest
from subscription_plans.mercadopago.mercadopago_subscription_request import MercadopagoSubscriptionRequest
from subscription_plans.mercadopago.mercadopago_subscription_request_params import MercadopagoSubscriptionRequestParams


class PaymentCreatedEvent(WebhookEvent):
    def __init__(self, data: dict, last_authorized_subscription: LastAuthorizedSubscriptionOf):
        self._data = data
        self._last_authorized_subscription = last_authorized_subscription

    @classmethod
    def create(cls, data: dict):
        payment_request = MercadopagoPaymentRequest.create(
            GetMethod(),
            data.get('data').get('id'),
            EmptyRequestBody()
        )
        subscription_request = MercadopagoSubscriptionRequest(
            GetMethod(),
            MercadopagoURL('preapproval/search'),
            EmptyRequestBody(),
            MercadopagoSubscriptionRequestParams(PayerEmail(payment_request), status='authorized'),
            DefaultMercadopagoHeaders()
        )
        return cls(data, LastAuthorizedSubscriptionOf(subscription_request))

    def dispatch(self):
        self._last_authorized_subscription.authorize()
        self._last_authorized_subscription.remove_pending()
