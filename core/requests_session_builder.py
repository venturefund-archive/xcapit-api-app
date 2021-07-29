import requests
from enum import Enum
from core.timeout_http_adapter import TimeoutHTTPAdapter
from requests.adapters import HTTPAdapter


class RequestsSessionBuilder:

    class Prefix(Enum):
        http = 'http://'
        https = 'https://'

    def __init__(self):
        self._session = requests.Session()

    @property
    def session(self):
        return self._session

    def set_timeout(self, timeout):
        self._mount(
            prefixes=[self.Prefix.http.value, self.Prefix.https.value],
            adapter=TimeoutHTTPAdapter(timeout=timeout)
        )
        return self

    def _mount(self, prefixes: list, adapter: HTTPAdapter):
        for prefix in prefixes:
            self._session.mount(prefix, adapter)
