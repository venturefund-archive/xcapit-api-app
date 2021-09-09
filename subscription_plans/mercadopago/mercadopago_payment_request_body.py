import json
from core.http.request_body import RequestBody


class MercadopagoPaymentRequestBody(RequestBody):
    def __init__(self, data: dict):
        self._data = data

    def json(self):
        return json.dumps(self._data)
