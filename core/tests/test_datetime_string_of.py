from datetime import datetime
from core.datetime.StringOf import StringOf
from core.datetime.datetime_of import DefaultDatetimeOf


def test_new():
    assert StringOf(
        DefaultDatetimeOf(a_string='2021-04-04 21:30:00', a_date_format='%Y-%m-%d %H:%M:%S'),
        a_date_format='%Y-%m-%dT%H:%M:%S.%fZ'
    )


def test_value_access():
    a_string_date = '2021-04-04 21:30:00'
    a_date_format = '%Y-%m-%d %H:%M:%S'
    another_date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    datetime_ = datetime.strptime(a_string_date, a_date_format)
    string_date_time = StringOf(DefaultDatetimeOf(a_string_date, a_date_format), another_date_format)

    assert string_date_time.value() == datetime_.strftime(another_date_format)
