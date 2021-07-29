class SortedSubscriptions:
    def __init__(self, subscriptions: list, key: callable):
        self._subscriptions = subscriptions
        self._key = key

    def _sorted(self):
        return sorted(self._subscriptions, key=self._key)

    def last(self):
        return [self._sorted().pop()] if len(self._sorted()) else []
