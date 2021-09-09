from requests import Response
from functools import lru_cache as cache

from core.http.empty_request_body import EmptyRequestBody
from core.http.empty_request_params import EmptyRequestParams
from core.http.request_body import RequestBody
from core.http.http_methods import HTTPMethod
from subscription_plans.mercadopago.mercadopago_url import MercadopagoURL
from subscription_plans.mercadopago.mercadopago_request import MercadopagoRequest
from subscription_plans.mercadopago.mercadopago_headers import DefaultMercadopagoHeaders
from core.http.request_headers import RequestHeaders
from core.http.request_params import RequestParams


class MercadopagoSubscriptionRequest(MercadopagoRequest):

    def __init__(
            self,
            method: HTTPMethod,
            url: MercadopagoURL,
            body: RequestBody,
            params: RequestParams,
            headers: RequestHeaders
    ):
        self._method = method
        self._url = url
        self._body = body
        self._params = params
        self._headers = headers

    @classmethod
    def create(
            cls,
            method: HTTPMethod,
            body: RequestBody = EmptyRequestBody(),
            params: RequestParams = EmptyRequestParams()
    ):
        return cls(method, MercadopagoURL('preapproval'), body, params, DefaultMercadopagoHeaders())

    @cache
    def response(self) -> Response:
        return self._method.fetch(
            self._url,
            data=self._body.json(),
            params=self._params.value(),
            headers=self._headers.value()
        )
