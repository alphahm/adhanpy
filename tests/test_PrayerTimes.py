import math
import pytest
from adhanpy.util.DateComponents import DateComponents
from adhanpy.calculation.CalculationMethod import CalculationMethod
from adhanpy.calculation.CalculationParameters import CalculationParameters
from adhanpy.astronomy.SolarTime import SolarTime
from adhanpy.util.TimeComponents import TimeComponents
from adhanpy.calculation.Madhab import Madhab
from adhanpy.PrayerTimes import PrayerTimes
from adhanpy.calculation.PrayerAdjustments import PrayerAdjustments
from zoneinfo import ZoneInfo


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


def test_either_calculation_method_or_calculation_parameters_is_passed():
    date = DateComponents(2015, 7, 12)
    method = CalculationMethod.NORTH_AMERICA
    params = CalculationParameters(method=method)
    coordinates = (35.7750, -78.6336)

    with pytest.raises(
        ValueError,
        match="Only one of calculation_method or calculation_parameters must be passed.",
    ):
        PrayerTimes(coordinates, date, method, params)


def test_when_transit_or_sunrise_components_or_sunset_components_or_tomorrow_sunrise_components_is_none_it_should_raise_exception(
    mocker,
):
    date = DateComponents(2015, 7, 12)
    mocker.patch.object(TimeComponents, "from_float", lambda e: None)
    method = CalculationMethod.NORTH_AMERICA
    coordinates = (35.7750, -78.6336)

    with pytest.raises(RuntimeError):
        PrayerTimes(coordinates, date, method)


def test_when_asr_is_not_set_raise_exception(mocker):
    date = DateComponents(2015, 7, 12)
    mocker.patch.object(SolarTime, "afternoon", lambda e, f: math.inf)
    method = CalculationMethod.NORTH_AMERICA
    coordinates = (35.7750, -78.6336)

    with pytest.raises(RuntimeError):
        PrayerTimes(coordinates, date, method)


def test_prayer_times_with_method_with_isha_interval():
    date = DateComponents(2022, 8, 8)
    parameters = CalculationParameters(method=CalculationMethod.UMM_AL_QURA)
    coordinates = (21.422510, 39.826168)

    prayer_times = PrayerTimes(coordinates, date, calculation_parameters=parameters)

    interval_maghrib_isha = prayer_times.isha - prayer_times.maghrib

    assert interval_maghrib_isha.total_seconds() / 60 == parameters.isha_interval


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
    # Values from http://www.moonsighting.com/pray.php
    # Arrange
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


def test_moon_sighting_method_high_lat_different_times_of_year():
    # Values from http://www.moonsighting.com/pray.php
    # Arrange
    params = CalculationParameters(method=CalculationMethod.MOON_SIGHTING_COMMITTEE)
    coordinates = (59.9094, 10.7349)
    format = "%I:%M %p"
    tz = ZoneInfo("Europe/Oslo")

    # Act, Assert
    date = DateComponents(2015, 7, 12)
    prayer_times = PrayerTimes(coordinates, date, calculation_parameters=params)
    assert prayer_times.fajr.astimezone(tz).strftime(format) == "03:26 AM"

    date = DateComponents(2015, 10, 12)
    prayer_times = PrayerTimes(coordinates, date, calculation_parameters=params)
    assert prayer_times.dhuhr.astimezone(tz).strftime(format) == "01:09 PM"

    date = DateComponents(2015, 4, 12)
    prayer_times = PrayerTimes(coordinates, date, calculation_parameters=params)
    assert prayer_times.asr.astimezone(tz).strftime(format) == "05:04 PM"

    date = DateComponents(2015, 5, 12)
    prayer_times = PrayerTimes(coordinates, date, calculation_parameters=params)
    assert prayer_times.maghrib.astimezone(tz).strftime(format) == "09:43 PM"

    date = DateComponents(2015, 9, 12)
    prayer_times = PrayerTimes(coordinates, date, calculation_parameters=params)
    assert prayer_times.isha.astimezone(tz).strftime(format) == "09:03 PM"


def test_prayer_times_timezone_conversion():
    # Arrange
    calculation_method = CalculationMethod.MOON_SIGHTING_COMMITTEE
    coordinates = (51.49799827422162, -0.1358135027951458)
    format = "%I:%M %p"
    tz = ZoneInfo("Europe/London")

    # Winter time, UTC and GMT share the same time
    date_winter = DateComponents(2022, 1, 1)

    # Summer time, BST: UTC + 1
    date_summer = DateComponents(2022, 8, 1)

    # Act,  Assert
    prayer_times = PrayerTimes(
        coordinates, date_winter, calculation_method=calculation_method
    )
    assert prayer_times.fajr.strftime(format) == "06:25 AM"

    prayer_times = PrayerTimes(
        coordinates, date_winter, calculation_method=calculation_method, time_zone=tz
    )
    assert prayer_times.fajr.strftime(format) == "06:25 AM"

    prayer_times = PrayerTimes(
        coordinates, date_summer, calculation_method=calculation_method
    )
    assert prayer_times.fajr.strftime(format) == "02:37 AM"

    prayer_times = PrayerTimes(
        coordinates, date_summer, calculation_method=calculation_method, time_zone=tz
    )
    assert prayer_times.fajr.strftime(format) == "03:37 AM"
