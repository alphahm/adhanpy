from datetime import datetime
from adhanpy.data.DateComponents import DateComponents
from adhanpy.CalculationMethod import CalculationMethod
from adhanpy.CalculationParameters import CalculationParameters
from adhanpy.Madhab import Madhab
from adhanpy.Coordinates import Coordinates
from adhanpy.PrayerTimes import PrayerTimes, days_since_solstice
from adhanpy.PrayerAdjustments import PrayerAdjustments
from zoneinfo import ZoneInfo


def test_days_since_solstice():
    _days_since_solstice_test(11, 2016, 1, 1, 1)
    _days_since_solstice_test(10, 2015, 12, 31, 1)
    _days_since_solstice_test(10, 2016, 12, 31, 1)
    _days_since_solstice_test(0, 2016, 12, 21, 1)
    _days_since_solstice_test(1, 2016, 12, 22, 1)
    _days_since_solstice_test(71, 2016, 3, 1, 1)
    _days_since_solstice_test(70, 2015, 3, 1, 1)
    _days_since_solstice_test(365, 2016, 12, 20, 1)
    _days_since_solstice_test(364, 2015, 12, 20, 1)

    _days_since_solstice_test(0, 2015, 6, 21, -1)
    _days_since_solstice_test(0, 2016, 6, 21, -1)
    _days_since_solstice_test(364, 2015, 6, 20, -1)
    _days_since_solstice_test(365, 2016, 6, 20, -1)

def test_PrayerTimes():
    date = DateComponents(2015, 7, 12)
    params = CalculationParameters()
    params.get_parameters_from_method(CalculationMethod.NORTH_AMERICA)

    params.madhab = Madhab.HANAFI
    coordinates = Coordinates(35.7750, -78.6336)
    prayer_times = PrayerTimes(coordinates, date, params)

    format = "%I:%M %p"
    tz = ZoneInfo("America/New_York")

    assert prayer_times.fajr.astimezone(tz).strftime(format) == "04:42 AM"
    assert prayer_times.sunrise.astimezone(tz).strftime(format) == "06:08 AM"
    assert prayer_times.dhuhr.astimezone(tz).strftime(format) == "01:21 PM"
    assert prayer_times.asr.astimezone(tz).strftime(format) == "06:22 PM"
    assert prayer_times.maghrib.astimezone(tz).strftime(format) == "08:32 PM"
    assert prayer_times.isha.astimezone(tz).strftime(format) == "09:57 PM"

def test_offsets():
    date = DateComponents(2015, 12, 1);
    coordinates = Coordinates(35.7750, -78.6336);

    format = "%I:%M %p"
    tz = ZoneInfo("America/New_York")

    parameters = CalculationParameters()
    parameters.get_parameters_from_method(CalculationMethod.MUSLIM_WORLD_LEAGUE)

    prayerTimes = PrayerTimes(coordinates, date, parameters)
    assert prayerTimes.fajr.astimezone(tz).strftime(format) == "05:35 AM"
    assert prayerTimes.sunrise.astimezone(tz).strftime(format) == "07:06 AM"
    assert prayerTimes.dhuhr.astimezone(tz).strftime(format) == "12:05 PM"
    assert prayerTimes.asr.astimezone(tz).strftime(format) == "02:42 PM"
    assert prayerTimes.maghrib.astimezone(tz).strftime(format) == "05:01 PM"
    assert prayerTimes.isha.astimezone(tz).strftime(format) == "06:26 PM"

    parameters.adjustments.fajr = 10
    parameters.adjustments.sunrise = 10
    parameters.adjustments.dhuhr = 10
    parameters.adjustments.asr = 10
    parameters.adjustments.maghrib = 10
    parameters.adjustments.isha = 10

    prayerTimes = PrayerTimes(coordinates, date, parameters)
    assert prayerTimes.fajr.astimezone(tz).strftime(format) == "05:45 AM"
    assert prayerTimes.sunrise.astimezone(tz).strftime(format) == "07:16 AM"
    assert prayerTimes.dhuhr.astimezone(tz).strftime(format) == "12:15 PM"
    assert prayerTimes.asr.astimezone(tz).strftime(format) == "02:52 PM"
    assert prayerTimes.maghrib.astimezone(tz).strftime(format) == "05:11 PM"
    assert prayerTimes.isha.astimezone(tz).strftime(format) == "06:36 PM"

    parameters.adjustments = PrayerAdjustments()
    prayerTimes = PrayerTimes(coordinates, date, parameters)
    assert prayerTimes.fajr.astimezone(tz).strftime(format) == "05:35 AM"
    assert prayerTimes.sunrise.astimezone(tz).strftime(format) == "07:06 AM"
    assert prayerTimes.dhuhr.astimezone(tz).strftime(format) == "12:05 PM"
    assert prayerTimes.asr.astimezone(tz).strftime(format) == "02:42 PM"
    assert prayerTimes.maghrib.astimezone(tz).strftime(format) == "05:01 PM"
    assert prayerTimes.isha.astimezone(tz).strftime(format) == "06:26 PM"


def test_moon_sighting_method():
    date = DateComponents(2016, 1, 31)
    coordinates = Coordinates(35.7750, -78.6336)

    parameters = CalculationParameters()
    parameters.get_parameters_from_method(CalculationMethod.MOON_SIGHTING_COMMITTEE)

    prayerTimes = PrayerTimes(coordinates, date, parameters)

    format = "%I:%M %p"
    tz = ZoneInfo("America/New_York")

    assert prayerTimes.fajr.astimezone(tz).strftime(format) == "05:48 AM"
    assert prayerTimes.sunrise.astimezone(tz).strftime(format) == "07:16 AM"
    assert prayerTimes.dhuhr.astimezone(tz).strftime(format) == "12:33 PM"
    assert prayerTimes.asr.astimezone(tz).strftime(format) == "03:20 PM"
    assert prayerTimes.maghrib.astimezone(tz).strftime(format) == "05:43 PM"
    assert prayerTimes.isha.astimezone(tz).strftime(format) == "07:05 PM"

def _days_since_solstice_test( value: int, year: int, month: int, day: int, latitude: float):
    """
    For Northern Hemisphere start from December 21
    (DYY=0 for December 21, and counting forward, DYY=11 for January 1 and so on).
    For Southern Hemisphere start from June 21
    (DYY=0 for June 21, and counting forward)
    """
    date = datetime(year, month, day)
    
    day_of_year = date.timetuple().tm_yday

    assert days_since_solstice(day_of_year, date.year, latitude) == value
