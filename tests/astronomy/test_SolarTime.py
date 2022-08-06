from datetime import datetime, timezone, timedelta
from adhanpy.data.Coordinates import Coordinates
from adhanpy.util.DateComponents import DateComponents
from adhanpy.util.TimeComponents import TimeComponents
from adhanpy.astronomy.SolarTime import SolarTime


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


def test_right_ascension_edge_case():
    coordinates = Coordinates(35 + 47.0 / 60.0, -78 - 39.0 / 60.0)

    for i in range(365):
        time = SolarTime(_make_date_with_offset(2016, 1, 1, i), coordinates)

        if i > 0:
            # transit from one day to another should not differ more than one minute
            assert abs(time.transit - previous_time.transit) < (1.0 / 60.0)

            # sunrise and sunset from one day to another should not differ more than two minutes
            assert abs(time.sunrise - previous_time.sunrise) < (2.0 / 60.0)
            assert abs(time.sunset - previous_time.sunset) < (2.0 / 60.0)

        previous_time = time


def test_calendrical_date():
    # generated from http://aa.usno.navy.mil/data/docs/RS_OneYear.php for KUKUIHAELE, HAWAII
    coordinates = Coordinates(20 + 7.0 / 60.0, -155.0 - 34.0 / 60.0)
    day1solar = SolarTime(DateComponents(2015, 4, 2), coordinates)
    day2solar = SolarTime(DateComponents(2015, 4, 3), coordinates)

    day1 = day1solar.sunrise
    day2 = day2solar.sunrise

    assert _time_string(day1) == "16:15"
    assert _time_string(day2) == "16:14"


def _make_date_with_offset(year: int, month: int, day: int, offset: int):
    date_time = datetime(year, month, day, tzinfo=timezone.utc)

    date_time_offset = date_time + timedelta(days=offset)
    return DateComponents.from_utc(date_time_offset)


def _time_string(when: float):
    components = TimeComponents.from_float(when)
    if components is None:
        return ""

    minutes = int((components.minutes + round(components.seconds / 60.0)))

    return f"{components.hours}:{minutes:0>2d}"
