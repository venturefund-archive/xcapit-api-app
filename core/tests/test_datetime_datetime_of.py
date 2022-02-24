from datetime import datetime
from core.datetime.datetime_of import DefaultDatetimeOf


def test_new():
    assert DefaultDatetimeOf(a_string='', a_date_format='')


def test_value_access():
    a_string_date = '2021-04-04 21:30:00'
    a_date_format = '%Y-%m-%d %H:%M:%S'
    date_time = DefaultDatetimeOf(a_string_date, a_date_format)

    assert date_time.value() == datetime.strptime(a_string_date, a_date_format)
