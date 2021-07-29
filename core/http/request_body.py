from abc import ABC, abstractmethod


class RequestBody(ABC):
    @abstractmethod
    def json(self):
        """"""
