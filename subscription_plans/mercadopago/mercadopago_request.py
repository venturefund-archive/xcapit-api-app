from requests import Response
from abc import abstractmethod, ABC


class MercadopagoRequest(ABC):
    @abstractmethod
    def response(self) -> Response:
        pass
