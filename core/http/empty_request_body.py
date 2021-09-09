import json
from core.http.request_body import RequestBody


class EmptyRequestBody(RequestBody):
    def __init__(self):
        self._empty_body = {}

    def json(self):
        return json.dumps(self._empty_body)
