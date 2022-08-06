from datetime import datetime
import pytest
from adhanpy.util.DateComponents import DateComponents
from adhanpy.calculation.CalculationMethod import CalculationMethod
from adhanpy.calculation.CalculationParameters import CalculationParameters
from adhanpy.calculation.Madhab import Madhab
from adhanpy.PrayerTimes import PrayerTimes, days_since_solstice
from adhanpy.calculation.PrayerAdjustments import PrayerAdjustments
from adhanpy.data.Prayer import Prayer
from adhanpy.calculation.HighLatitudeRule import HighLatitudeRule
from zoneinfo import ZoneInfo


@pytest.mark.parametrize(
    "year, month, day, latitude, expected",
    [
        (2016, 1, 1, 1, 11),
        (2015, 12, 31, 1, 10),
        (2016, 12, 31, 1, 10),
        (2016, 12, 21, 1, 0),
        (2016, 12, 22, 1, 1),
        (2016, 3, 1, 1, 71),
        (2015, 3, 1, 1, 70),
        (2016, 12, 20, 1, 365),
        (2015, 12, 20, 1, 364),
        (2015, 6, 21, -1, 0),
        (2016, 6, 21, -1, 0),
        (2015, 6, 20, -1, 364),
        (2016, 6, 20, -1, 365),
    ],
)
def test_days_since_solstice(year, month, day, latitude, expected):
    """
    For Northern Hemisphere start from December 21
    (DYY=0 for December 21, and counting forward, DYY=11 for January 1 and so on).
    For Southern Hemisphere start from June 21
    (DYY=0 for June 21, and counting forward)
    """

    # Arrange
    date = datetime(year, month, day)
    day_of_year = date.timetuple().tm_yday

    # Act, Assert
    assert days_since_solstice(day_of_year, date.year, latitude) == expected


def test_PrayerTimes():
    # Arrange
    date = DateComponents(2015, 7, 12)
    params = CalculationParameters(method=CalculationMethod.NORTH_AMERICA)
    params.madhab = Madhab.HANAFI
    coordinates = (35.7750, -78.6336)
    format = "%I:%M %p"
    tz = ZoneInfo("America/New_York")

    # Act
    prayer_times = PrayerTimes(coordinates, date, calculation_parameters=params)

    # Assert
    assert prayer_times.fajr.astimezone(tz).strftime(format) == "04:42 AM"
    assert prayer_times.sunrise.astimezone(tz).strftime(format) == "06:08 AM"
    assert prayer_times.dhuhr.astimezone(tz).strftime(format) == "01:21 PM"
    assert prayer_times.asr.astimezone(tz).strftime(format) == "06:22 PM"
    assert prayer_times.maghrib.astimezone(tz).strftime(format) == "08:32 PM"
    assert prayer_times.isha.astimezone(tz).strftime(format) == "09:57 PM"


def test_offsets():
    # Arrange
    date = DateComponents(2015, 12, 1)
    coordinates = (35.7750, -78.6336)
    format = "%I:%M %p"
    tz = ZoneInfo("America/New_York")
    calculation_method = CalculationMethod.MUSLIM_WORLD_LEAGUE

    parameters_with_no_offsets = CalculationParameters(method=calculation_method)

    parameters_with_offsets = CalculationParameters(method=calculation_method)
    parameters_with_offsets.adjustments.fajr = 10
    parameters_with_offsets.adjustments.sunrise = 10
    parameters_with_offsets.adjustments.dhuhr = 10
    parameters_with_offsets.adjustments.asr = 10
    parameters_with_offsets.adjustments.maghrib = 10
    parameters_with_offsets.adjustments.isha = 10

    parameters_with_blank_adjustments = CalculationParameters(method=calculation_method)
    parameters_with_blank_adjustments.adjustments = PrayerAdjustments()

    # Act
    prayer_times_with_no_offsets = PrayerTimes(
        coordinates, date, calculation_parameters=parameters_with_no_offsets
    )
    prayer_times_with_offsets = PrayerTimes(
        coordinates, date, calculation_parameters=parameters_with_offsets
    )
    prayer_times_with_blank_adjustments = PrayerTimes(
        coordinates, date, calculation_parameters=parameters_with_blank_adjustments
    )

    # Assert
    assert (
        prayer_times_with_no_offsets.fajr.astimezone(tz).strftime(format) == "05:35 AM"
    )
    assert prayer_times_with_offsets.fajr.astimezone(tz).strftime(format) == "05:45 AM"
    assert (
        prayer_times_with_blank_adjustments.fajr.astimezone(tz).strftime(format)
        == "05:35 AM"
    )

    assert (
        prayer_times_with_no_offsets.sunrise.astimezone(tz).strftime(format)
        == "07:06 AM"
    )
    assert (
        prayer_times_with_offsets.sunrise.astimezone(tz).strftime(format) == "07:16 AM"
    )
    assert (
        prayer_times_with_blank_adjustments.sunrise.astimezone(tz).strftime(format)
        == "07:06 AM"
    )

    assert (
        prayer_times_with_no_offsets.dhuhr.astimezone(tz).strftime(format) == "12:05 PM"
    )
    assert prayer_times_with_offsets.dhuhr.astimezone(tz).strftime(format) == "12:15 PM"
    assert prayer_times_with_blank_adjustments

    assert (
        prayer_times_with_no_offsets.asr.astimezone(tz).strftime(format) == "02:42 PM"
    )
    assert prayer_times_with_offsets.asr.astimezone(tz).strftime(format) == "02:52 PM"
    assert (
        prayer_times_with_blank_adjustments.asr.astimezone(tz).strftime(format)
        == "02:42 PM"
    )

    assert (
        prayer_times_with_no_offsets.maghrib.astimezone(tz).strftime(format)
        == "05:01 PM"
    )
    assert (
        prayer_times_with_offsets.maghrib.astimezone(tz).strftime(format) == "05:11 PM"
    )
    assert (
        prayer_times_with_blank_adjustments.maghrib.astimezone(tz).strftime(format)
        == "05:01 PM"
    )

    assert (
        prayer_times_with_no_offsets.isha.astimezone(tz).strftime(format) == "06:26 PM"
    )
    assert prayer_times_with_offsets.isha.astimezone(tz).strftime(format) == "06:36 PM"
    assert (
        prayer_times_with_blank_adjustments.isha.astimezone(tz).strftime(format)
        == "06:26 PM"
    )


def test_moon_sighting_method():
    # Arrange
    date = DateComponents(2016, 1, 31)
    coordinates = (35.7750, -78.6336)
    calculation_method = CalculationMethod.MOON_SIGHTING_COMMITTEE
    format = "%I:%M %p"
    tz = ZoneInfo("America/New_York")

    # Act
    prayer_times = PrayerTimes(coordinates, date, calculation_method)

    # Assert
    assert prayer_times.fajr.astimezone(tz).strftime(format) == "05:48 AM"
    assert prayer_times.sunrise.astimezone(tz).strftime(format) == "07:16 AM"
    assert prayer_times.dhuhr.astimezone(tz).strftime(format) == "12:33 PM"
    assert prayer_times.asr.astimezone(tz).strftime(format) == "03:20 PM"
    assert prayer_times.maghrib.astimezone(tz).strftime(format) == "05:43 PM"
    assert prayer_times.isha.astimezone(tz).strftime(format) == "07:05 PM"


def test_moon_sighting_method_high_lat():
    # Arrange
    # Values from http://www.moonsighting.com/pray.php
    date = DateComponents(2016, 1, 1)
    parameters = CalculationParameters(method=CalculationMethod.MOON_SIGHTING_COMMITTEE)
    parameters.madhab = Madhab.HANAFI
    coordinates = (59.9094, 10.7349)
    format = "%I:%M %p"
    tz = ZoneInfo("Europe/Oslo")

    # Act
    prayer_times = PrayerTimes(coordinates, date, calculation_parameters=parameters)

    # Assert
    assert prayer_times.fajr.astimezone(tz).strftime(format) == "07:34 AM"
    assert prayer_times.sunrise.astimezone(tz).strftime(format) == "09:19 AM"
    assert prayer_times.dhuhr.astimezone(tz).strftime(format) == "12:25 PM"
    assert prayer_times.asr.astimezone(tz).strftime(format) == "01:36 PM"
    assert prayer_times.maghrib.astimezone(tz).strftime(format) == "03:25 PM"
    assert prayer_times.isha.astimezone(tz).strftime(format) == "05:02 PM"


def test_time_for_prayer():
    # Arrange
    date = DateComponents(2016, 7, 1)
    parameters = CalculationParameters(method=CalculationMethod.MUSLIM_WORLD_LEAGUE)
    parameters.madhab = Madhab.HANAFI
    parameters.high_latitude_rule = HighLatitudeRule.TWILIGHT_ANGLE
    coordinates = (59.9094, 10.7349)

    # Act
    prayer_times = PrayerTimes(coordinates, date, calculation_parameters=parameters)

    # Assert
    assert prayer_times.fajr == prayer_times.time_for_prayer(Prayer.FAJR)
    assert prayer_times.sunrise == prayer_times.time_for_prayer(Prayer.SUNRISE)
    assert prayer_times.dhuhr == prayer_times.time_for_prayer(Prayer.DHUHR)
    assert prayer_times.asr == prayer_times.time_for_prayer(Prayer.ASR)
    assert prayer_times.maghrib == prayer_times.time_for_prayer(Prayer.MAGHRIB)
    assert prayer_times.isha == prayer_times.time_for_prayer(Prayer.ISHA)
    assert prayer_times.time_for_prayer(Prayer.NONE) is None
