from datetime import datetime
from core.value import Value


class DatetimeOf(Value):

    def __init__(self, a_string: str, a_date_format: str = '%Y-%m-%dT%H:%M:%S.%fZ'):
        self._a_date_format = a_date_format
        self._a_string = a_string

    def value(self) -> datetime:
        return datetime.strptime(self._a_string, self._a_date_format)
