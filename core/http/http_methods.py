from requests import Response, Request
from unittest.mock import Mock
from abc import abstractmethod, ABC
from api_app.settings import DEFAULT_REQUEST_TIMEOUT
from core.requests_session_builder import RequestsSessionBuilder


class HTTPMethod(ABC):
    def __init__(self):
        self._requests = RequestsSessionBuilder().set_timeout(DEFAULT_REQUEST_TIMEOUT).session

    @abstractmethod
    def fetch(self, *args, **kwargs):
        pass


class PostMethod(HTTPMethod):

    def fetch(self, *args, **kwargs):
        return self._requests.post(*args, **kwargs)


class GetMethod(HTTPMethod):

    def fetch(self, *args, **kwargs):
        return self._requests.get(*args, **kwargs)


class FakeHTTPMethod(HTTPMethod):
    def __init__(self, status_code=200, json_res=None):
        self._status_code = status_code
        self._json_res = json_res or {}
        super().__init__()

    def fetch(self, *args, **kwargs):
        return Mock(
            spec=Response,
            status_code=self._status_code,
            json=lambda: self._json_res
        )
