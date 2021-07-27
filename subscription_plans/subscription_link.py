from requests import Response


class SubscriptionLink:
    def __init__(self, response: Response):
        self._response = response

    def value(self):
        return self._response.json().get('init_point')
