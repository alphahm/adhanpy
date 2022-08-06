import pytest
import adhanpy.astronomy.CalendricalHelper as CalendricalHelper


@pytest.mark.parametrize(
    "year, month, day, expected",
    [
        (2010, 1, 2, 2455198.500000),
        (2011, 2, 4, 2455596.500000),
        (2012, 3, 6, 2455992.500000),
        (2013, 4, 8, 2456390.500000),
        (2014, 5, 10, 2456787.500000),
        (2015, 6, 12, 2457185.500000),
        (2016, 7, 14, 2457583.500000),
        (2017, 8, 16, 2457981.500000),
        (2018, 9, 18, 2458379.500000),
        (2019, 10, 20, 2458776.500000),
        (2020, 11, 22, 2459175.500000),
        (2021, 12, 24, 2459572.500000),
    ],
)
def test_julian_day(year, month, day, expected):
    # Comparison values generated from http://aa.usno.navy.mil/data/docs/JulianDate.php

    assert CalendricalHelper.julian_day(year, month, day) == pytest.approx(
        expected, abs=1e-5
    )


def test_julian_day_with_hours_and_minutes():
    # Comparison values generated from http://aa.usno.navy.mil/data/docs/JulianDate.php

    jdVal = 2457215.67708333
    assert CalendricalHelper.julian_day(2015, 7, 12, 4.25) == pytest.approx(
        jdVal, abs=1e-6
    )
    assert CalendricalHelper.julian_day(2015, 7, 12, 4, 15) == pytest.approx(
        jdVal, abs=1e-6
    )
    assert CalendricalHelper.julian_day(2015, 7, 12, 8.0) == pytest.approx(
        2457215.833333, abs=1e-6
    )
    assert CalendricalHelper.julian_day(1992, 10, 13, 0.0) == pytest.approx(
        2448908.5, abs=1e-6
    )


def test_julian_hours():
    j1 = CalendricalHelper.julian_day(2010, 1, 3)
    j2 = CalendricalHelper.julian_day(2010, 1, 1, 48)

    assert j1 == pytest.approx(j2, abs=1e-7)
