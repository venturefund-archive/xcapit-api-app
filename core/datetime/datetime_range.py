from core.datetime.datetime_of import DatetimeOf


class DatetimeRange:

    def __init__(self, since: DatetimeOf = None, to: DatetimeOf = None):
        self._to = to
        self._since = since

    def since(self) -> DatetimeOf:
        return self._since

    def to(self) -> DatetimeOf:
        return self._to
