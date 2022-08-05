import pytest
from datetime import datetime, timezone, timedelta
import adhanpy.internal.Astronomical as Astronomical
import adhanpy.internal.FloatUtil as FloatUtil
import adhanpy.internal.CalendricalHelper as CalendricalHelper
from adhanpy.internal.SolarCoordinates import SolarCoordinates
from adhanpy.Coordinates import Coordinates
from adhanpy.data.DateComponents import DateComponents
from adhanpy.data.TimeComponents import TimeComponents
from adhanpy.internal.SolarTime import SolarTime


def test_solar_coordinates():

    # values from Astronomical Algorithms page 165
    jd = CalendricalHelper.julian_day(1992, 10, 13)
    solar = SolarCoordinates(jd)

    T = CalendricalHelper.julian_century(jd)
    L0 = Astronomical.mean_solar_longitude(T)
    ε0 = Astronomical.mean_obliquity_of_the_ecliptic(T)
    εapp = Astronomical.apparent_obliquity_of_the_ecliptic(T, ε0)
    M = Astronomical.mean_solar_anomaly(T)
    C = Astronomical.solar_equation_of_the_center(T, M)
    λ = Astronomical.apparent_solar_longitude(T, L0)
    δ = solar.declination
    α = FloatUtil.unwind_angle(solar.right_ascension)

    assert T == pytest.approx(-0.072183436, abs=1e-11)
    assert L0 == pytest.approx(201.80720, abs=1e-5)
    assert ε0 == pytest.approx(23.44023, abs=1e-5)
    assert εapp == pytest.approx(23.43999, abs=1e-5)
    assert M == pytest.approx(278.99397, abs=1e-5)
    assert C == pytest.approx(-1.89732, abs=1e-5)

    # lower accuracy than desired
    assert λ == pytest.approx(199.90895, abs=2e-5)
    assert δ == pytest.approx(-7.78507, abs=1e-5)
    assert α == pytest.approx(198.38083, abs=1e-5)

    # values from Astronomical Algorithms page 88
    jd = CalendricalHelper.julian_day(1987, 4, 10)
    solar = SolarCoordinates(jd)
    T = CalendricalHelper.julian_century(jd)

    θ0 = Astronomical.mean_sidereal_time(T)
    θapp = solar.apparent_sidereal_time
    Ω = Astronomical.ascending_lunar_node_longitude(T)
    ε0 = Astronomical.mean_obliquity_of_the_ecliptic(T)
    L0 = Astronomical.mean_solar_longitude(T)
    Lp = Astronomical.mean_lunar_longitude(T)
    ΔΨ = Astronomical.nutation_in_longitude(T, L0, Lp, Ω)
    Δε = Astronomical.nutation_in_obliquity(T, L0, Lp, Ω)
    ε = ε0 + Δε

    assert θ0 == pytest.approx(197.693195, abs=1e-6)
    assert θapp == pytest.approx(197.6922295833, abs=1e-4)

    # values from Astronomical Algorithms page 148
    assert Ω == pytest.approx(11.2531, abs=1e-4)
    assert ΔΨ == pytest.approx(-0.0010522, abs=1e-4)
    assert Δε == pytest.approx(0.0026230556, abs=1e-5)
    assert ε0 == pytest.approx(23.4409463889, abs=1e-6)
    assert ε == pytest.approx(23.4435694444, abs=1e-5)


def test_right_ascension_edge_case():
    # SolarTime previousTime = null;
    coordinates = Coordinates(35 + 47.0 / 60.0, -78 - 39.0 / 60.0)

    for i in range(365):
        time = SolarTime(_makeDateWithOffset(2016, 1, 1, i), coordinates)

        if i > 0:
            # transit from one day to another should not differ more than one minute
            assert abs(time.transit - previous_time.transit) < (1.0 / 60.0)

            # sunrise and sunset from one day to another should not differ more than two minutes
            assert abs(time.sunrise - previous_time.sunrise) < (2.0 / 60.0)
            assert abs(time.sunset - previous_time.sunset) < (2.0 / 60.0)

        previous_time = time


def test_altitude_of_celestial_body():
    φ = 38 + (55 / 60.0) + (17.0 / 3600)
    δ = -6 - (43 / 60.0) - (11.61 / 3600)
    H = 64.352133
    h = Astronomical.altitude_of_celestial_body(φ, δ, H)
    assert h == pytest.approx(15.1249, abs=1e-4)


def test_transit_and_hour_angle():
    # alues from Astronomical Algorithms page 103
    longitude = -71.0833
    Θ = 177.74208
    α1 = 40.68021
    α2 = 41.73129
    α3 = 42.78204
    m0 = Astronomical.approximate_transit(longitude, Θ, α2)

    assert m0 == pytest.approx(0.81965, abs=1e-5)

    transit = Astronomical.corrected_transit(m0, longitude, Θ, α2, α1, α3) / 24

    assert transit == pytest.approx(0.81980, abs=1e-5)

    δ1 = 18.04761
    δ2 = 18.44092
    δ3 = 18.82742

    rise = (
        Astronomical.corrected_hour_angle(
            m0,
            -0.5667,
            Coordinates(42.3333, longitude),
            False,
            Θ,
            α2,
            α1,
            α3,
            δ2,
            δ1,
            δ3,
        )
        / 24
    )
    assert rise == pytest.approx(0.51766, abs=1e-5)


def test_solar_time():
    """
    Comparison values generated from
    http://aa.usno.navy.mil/rstt/onedaytable?form=1&ID=AA&year=2015&month=7&day=12&state=NC&place=raleigh
    """

    coordinates = Coordinates(35 + 47.0 / 60.0, -78 - 39.0 / 60.0)
    solar = SolarTime(DateComponents(2015, 7, 12), coordinates)

    transit = solar.transit
    sunrise = solar.sunrise
    sunset = solar.sunset
    twilight_start = solar.hour_angle(-6, False)
    twilight_end = solar.hour_angle(-6, True)
    invalid = solar.hour_angle(-36, True)

    assert _time_string(twilight_start) == "9:38"
    assert _time_string(sunrise) == "10:08"
    assert _time_string(transit) == "17:20"
    assert _time_string(sunset) == "24:32"
    assert _time_string(twilight_end) == "25:02"
    assert _time_string(invalid) == ""


def test_calendrical_date():
    # generated from http://aa.usno.navy.mil/data/docs/RS_OneYear.php for KUKUIHAELE, HAWAII
    coordinates = Coordinates(20 + 7.0 / 60.0, -155.0 - 34.0 / 60.0)
    day1solar = SolarTime(DateComponents(2015, 4, 2), coordinates)
    day2solar = SolarTime(DateComponents(2015, 4, 3), coordinates)

    day1 = day1solar.sunrise
    day2 = day2solar.sunrise

    assert _time_string(day1) == "16:15"
    assert _time_string(day2) == "16:14"


def test_interpolation():
    # values from Astronomical Algorithms page 25
    interpolatedValue = Astronomical.interpolate(
        0.877366, 0.884226, 0.870531, 4.35 / 24
    )

    assert interpolatedValue == pytest.approx(0.876125, abs=1e-6)

    i1 = Astronomical.interpolate(1, -1, 3, 0.6)
    assert i1 == pytest.approx(2.2, abs=1e-6)


def test_angle_interpolation():
    i1 = Astronomical.interpolate_angles(1, -1, 3, 0.6)
    assert i1 == pytest.approx(2.2, abs=1e-6)

    i2 = Astronomical.interpolate_angles(1, 359, 3, 0.6)
    assert i2 == pytest.approx(2.2, abs=1e-6)


def test_julian_day():
    # Comparison values generated from http://aa.usno.navy.mil/data/docs/JulianDate.php

    assert CalendricalHelper.julian_day(2010, 1, 2) == pytest.approx(
        2455198.500000, abs=1e-5
    )
    assert CalendricalHelper.julian_day(2011, 2, 4) == pytest.approx(
        2455596.500000, abs=1e-5
    )
    assert CalendricalHelper.julian_day(2012, 3, 6) == pytest.approx(
        2455992.500000, abs=1e-5
    )
    assert CalendricalHelper.julian_day(2013, 4, 8) == pytest.approx(
        2456390.500000, abs=1e-5
    )
    assert CalendricalHelper.julian_day(2014, 5, 10) == pytest.approx(
        2456787.500000, abs=1e-5
    )
    assert CalendricalHelper.julian_day(2015, 6, 12) == pytest.approx(
        2457185.500000, abs=1e-5
    )
    assert CalendricalHelper.julian_day(2016, 7, 14) == pytest.approx(
        2457583.500000, abs=1e-5
    )
    assert CalendricalHelper.julian_day(2017, 8, 16) == pytest.approx(
        2457981.500000, abs=1e-5
    )
    assert CalendricalHelper.julian_day(2018, 9, 18) == pytest.approx(
        2458379.500000, abs=1e-5
    )
    assert CalendricalHelper.julian_day(2019, 10, 20) == pytest.approx(
        2458776.500000, abs=1e-5
    )
    assert CalendricalHelper.julian_day(2020, 11, 22) == pytest.approx(
        2459175.500000, abs=1e-5
    )
    assert CalendricalHelper.julian_day(2021, 12, 24) == pytest.approx(
        2459572.500000, abs=1e-5
    )

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


def _time_string(when: float):
    components = TimeComponents.from_float(when)
    if components is None:
        return ""

    minutes = int((components.minutes + round(components.seconds / 60.0)))

    return f"{components.hours}:{minutes:0>2d}"


def _makeDateWithOffset(year: int, month: int, day: int, offset: int):
    date_time = datetime(year, month, day, tzinfo=timezone.utc)

    date_time_offset = date_time + timedelta(days=offset)
    return DateComponents.from_utc(date_time_offset)
