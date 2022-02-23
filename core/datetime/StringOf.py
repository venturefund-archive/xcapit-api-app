from core.datetime.datetime_of import DatetimeOf
from core.value import Value


class StringOf(Value):

    def __init__(self, a_datetime: DatetimeOf, a_date_format: str = '%d/%m/%Y %H:%M:%S'):
        self._a_date_format = a_date_format
        self._a_datetime = a_datetime

    def value(self) -> str:
        return self._a_datetime.value().strftime(self._a_date_format)
