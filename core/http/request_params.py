from abc import abstractmethod, ABC


class RequestParams(ABC):
    @abstractmethod
    def value(self):
        """"""
