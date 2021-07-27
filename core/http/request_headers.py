from abc import abstractmethod, ABC


class RequestHeaders(ABC):
    @abstractmethod
    def value(self):
        pass
