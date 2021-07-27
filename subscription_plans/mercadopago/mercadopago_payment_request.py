from requests import Response
from functools import lru_cache as cache
from core.http.http_methods import HTTPMethod
from core.http.request_body import RequestBody
from subscription_plans.mercadopago.mercadopago_url import MercadopagoURL
from subscription_plans.mercadopago.mercadopago_request import MercadopagoRequest
from subscription_plans.mercadopago.mercadopago_headers import DefaultMercadopagoHeaders


class MercadopagoPaymentRequest(MercadopagoRequest):
    def __init__(
            self,
            method: HTTPMethod,
            url: MercadopagoURL,
            body: RequestBody,
            headers: DefaultMercadopagoHeaders
    ):
        self._method = method
        self._url = url
        self._body = body
        self._headers = headers

    @classmethod
    def create(cls, method: HTTPMethod, payment_id: int, body: RequestBody):
        return cls(method, MercadopagoURL(f'v1/payments/{payment_id}'), body, DefaultMercadopagoHeaders())

    @cache
    def response(self) -> Response:
        return self._method.fetch(self._url, data=self._body.json(), headers=self._headers.value())
