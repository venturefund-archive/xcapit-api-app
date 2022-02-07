import pytest
from core.datetime.datetime_of import DatetimeOf
from core.datetime.datetime_range import DatetimeRange


@pytest.fixture
def since_datetime():
    return DatetimeOf('2021-04-04T21:30:00Z')


@pytest.fixture
def to_datetime():
    return DatetimeOf('2021-04-05T21:30:00Z')


def test_new(since_datetime, to_datetime):
    assert DatetimeRange()
    assert DatetimeRange(to=to_datetime)
    assert DatetimeRange(since=since_datetime)
    assert DatetimeRange(since=since_datetime, to=to_datetime)


def test_access_from_and_to(since_datetime, to_datetime):
    datetime_range = DatetimeRange(since=since_datetime, to=to_datetime)

    assert datetime_range.since() == since_datetime
    assert datetime_range.to() == to_datetime
