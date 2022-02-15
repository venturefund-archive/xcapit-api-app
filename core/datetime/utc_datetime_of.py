import pytz
from datetime import datetime
from core.datetime.datetime_of import DatetimeOf


class UTCDatetimeOf(DatetimeOf):

    def __init__(self, a_datetime_of: DatetimeOf):
        self._a_datetime_of = a_datetime_of

    def value(self) -> datetime:
        return self._a_datetime_of.value().astimezone(pytz.utc)
