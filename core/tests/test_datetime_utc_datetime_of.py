import pytz
import pytest
from datetime import datetime
from core.datetime.datetime_of import DefaultDatetimeOf
from core.datetime.utc_datetime_of import UTCDatetimeOf


def test_new():
    assert UTCDatetimeOf(DefaultDatetimeOf(a_string=''))


def test_value_access():
    a_string_date = '2021-04-04 00:00:00'
    a_date_format = '%Y-%m-%d %H:%M:%S'
    utc_datetime = UTCDatetimeOf(DefaultDatetimeOf(a_string_date, a_date_format))

    assert utc_datetime.value() == datetime(2021, 4, 4, tzinfo=pytz.utc)
