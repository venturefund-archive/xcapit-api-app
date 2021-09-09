from core.http.request_params import RequestParams


class EmptyRequestParams(RequestParams):
    def value(self):
        return {}
