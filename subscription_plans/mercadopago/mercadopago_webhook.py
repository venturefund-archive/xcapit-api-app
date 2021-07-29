class MercadopagoWebhook:
    def __init__(self, data: dict, events: dict):
        self._data = data
        self._events = events

    @property
    def action(self):
        return self._data.get('action')

    def dispatch_events(self):
        self._events.get(self.action)(self._data).dispatch()
