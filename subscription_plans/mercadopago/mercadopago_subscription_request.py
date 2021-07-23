from requests import Response
from functools import lru_cache as cache
from subscription_plans.http_methods import HTTPMethod
from subscription_plans.mercadopago.mercadopago_url import MercadopagoURL
from subscription_plans.mercadopago.mercadopago_request import MercadopagoRequest
from subscription_plans.mercadopago.mercadopago_headers import DefaultMercadopagoHeaders
from subscription_plans.mercadopago.mercadopago_subscription_request_body import MercadopagoSubscriptionRequestBody


class MercadopagoSubscriptionRequest(MercadopagoRequest):

    def __init__(
            self,
            method: HTTPMethod,
            url: MercadopagoURL,
            body: MercadopagoSubscriptionRequestBody,
            headers: DefaultMercadopagoHeaders
    ):
        self._method = method
        self._url = url
        self._body = body
        self._headers = headers

    @classmethod
    def create(cls, method: HTTPMethod, body: MercadopagoSubscriptionRequestBody):
        return cls(method, MercadopagoURL('preapproval'), body, DefaultMercadopagoHeaders())

    @cache
    def response(self) -> Response:
        return self._method.fetch(self._url, data=self._body.json(), headers=self._headers.value())
