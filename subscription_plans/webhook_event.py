from abc import abstractmethod, ABC


class WebhookEvent(ABC):
    @abstractmethod
    def dispatch(self):
        pass


class FakeWebhookEvent(WebhookEvent):
    def __init__(self, data: dict):
        self._data = data

    def dispatch(self):
        pass
