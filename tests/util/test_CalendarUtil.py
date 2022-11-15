from datetime import datetime, timezone
import adhanpy.util.CalendarUtil as CalendarUtil


def test_rounding_when_second_is_less_than_30():
    dt = datetime(2015, 1, 1, 10, 2, 29, tzinfo=timezone.utc)
    rounded = CalendarUtil.rounded_minute(dt)

    assert rounded.minute == 2
    assert rounded.second == 0


def test_rounding_when_second_is_greater_than_30():
    dt = datetime(2015, 1, 1, 10, 2, 31)
    rounded = CalendarUtil.rounded_minute(dt)

    assert rounded.minute == 3
    assert rounded.second == 0


def test_rounding_when_second_is_greater_than_30_and_minute_is_59():
    dt = datetime(2015, 1, 1, 10, 59, 31, tzinfo=timezone.utc)
    rounded = CalendarUtil.rounded_minute(dt)

    assert rounded.hour == 10
    assert rounded.minute == 59
    assert rounded.second == 0
