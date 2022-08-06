import pytest
from datetime import datetime, timezone
import adhanpy.util.FloatUtil as FloatUtil
from adhanpy.util.TimeComponents import TimeComponents
import adhanpy.util.CalendarUtil as CalendarUtil


def test_normalizing():
    assert FloatUtil.normalize_with_bound(2.0, -5) == pytest.approx(-3, abs=1e-5)
    assert FloatUtil.normalize_with_bound(-4.0, -5.0) == pytest.approx(-4, abs=1e-5)
    assert FloatUtil.normalize_with_bound(-6.0, -5.0) == pytest.approx(-1, abs=1e-5)

    assert FloatUtil.normalize_with_bound(-1.0, 24) == pytest.approx(23, abs=1e-5)
    assert FloatUtil.normalize_with_bound(1.0, 24.0) == pytest.approx(1, abs=1e-5)
    assert FloatUtil.normalize_with_bound(49.0, 24) == pytest.approx(1, abs=1e-5)

    assert FloatUtil.normalize_with_bound(361.0, 360) == pytest.approx(1, abs=1e-5)
    assert FloatUtil.normalize_with_bound(360.0, 360) == pytest.approx(0, abs=1e-5)
    assert FloatUtil.normalize_with_bound(259.0, 360) == pytest.approx(259, abs=1e-5)
    assert FloatUtil.normalize_with_bound(2592.0, 360) == pytest.approx(72, abs=1e-5)

    assert FloatUtil.unwind_angle(-45.0) == pytest.approx(315, abs=1e-5)
    assert FloatUtil.unwind_angle(361.0) == pytest.approx(1, abs=1e-5)
    assert FloatUtil.unwind_angle(360.0) == pytest.approx(0, abs=1e-5)
    assert FloatUtil.unwind_angle(259.0) == pytest.approx(259, abs=1e-5)
    assert FloatUtil.unwind_angle(2592.0) == pytest.approx(72, abs=1e-5)

    assert FloatUtil.normalize_with_bound(360.1, 360) == pytest.approx(0.1, abs=1e-2)


def test_closest_angle():
    assert FloatUtil.closest_angle(360.0) == pytest.approx(0, abs=1e-6)
    assert FloatUtil.closest_angle(361.0) == pytest.approx(1, abs=1e-6)
    assert FloatUtil.closest_angle(1.0) == pytest.approx(1, abs=1e-6)
    assert FloatUtil.closest_angle(-1.0) == pytest.approx(-1, abs=1e-6)
    assert FloatUtil.closest_angle(-181.0) == pytest.approx(179, abs=1e-6)
    assert FloatUtil.closest_angle(180.0) == pytest.approx(180, abs=1e-6)
    assert FloatUtil.closest_angle(359.0) == pytest.approx(-1, abs=1e-6)
    assert FloatUtil.closest_angle(-359.0) == pytest.approx(1, abs=1e-6)
    assert FloatUtil.closest_angle(1261.0) == pytest.approx(-179, abs=1e-6)
    assert FloatUtil.closest_angle(-360.1) == pytest.approx(-0.1, abs=1e-2)


def test_TimeComponents():
    comps1 = TimeComponents.from_float(15.199)
    assert comps1 is not None
    assert comps1.hours == 15
    assert comps1.minutes == 11
    assert comps1.seconds == 56

    comps2 = TimeComponents.from_float(1.0084)
    assert comps2 is not None
    assert comps2.hours == 1
    assert comps2.minutes == 0
    assert comps2.seconds == 30

    comps3 = TimeComponents.from_float(1.0083)
    assert comps3 is not None
    assert comps3.hours == 1
    assert comps3.minutes == 0

    comps4 = TimeComponents.from_float(2.1)
    assert comps4 is not None
    assert comps4.hours == 2
    assert comps4.minutes == 6

    comps5 = TimeComponents.from_float(3.5)
    assert comps5 is not None
    assert comps5.hours == 3
    assert comps5.minutes == 30


def testMinuteRounding():
    comps1 = datetime(2015, 1, 1, 10, 2, 29, tzinfo=timezone.utc)
    rounded1 = CalendarUtil.rounded_minute(comps1)

    assert rounded1.minute == 2
    assert rounded1.second == 0

    comps2 = datetime(2015, 1, 1, 10, 2, 31)
    rounded2 = CalendarUtil.rounded_minute(comps2)

    assert rounded2.minute == 3
    assert rounded2.second == 0
