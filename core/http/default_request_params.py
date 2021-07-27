from core.http.request_params import RequestParams


class DefaultRequestParams(RequestParams):
    def __init__(self, params: dict):
        self._params = params

    def value(self):
        return self._params
