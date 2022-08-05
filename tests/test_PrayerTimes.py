from datetime import datetime
from adhanpy.data.DateComponents import DateComponents
from adhanpy.CalculationMethod import CalculationMethod
from adhanpy.CalculationParameters import CalculationParameters
from adhanpy.Madhab import Madhab
from adhanpy.Coordinates import Coordinates
from adhanpy.PrayerTimes import PrayerTimes, days_since_solstice
from zoneinfo import ZoneInfo


def test_days_since_solstice():
    days_since_solstice_test(11, 2016, 1, 1, 1)
    days_since_solstice_test(10, 2015, 12, 31, 1)
    days_since_solstice_test(10, 2016, 12, 31, 1)
    days_since_solstice_test(0, 2016, 12, 21, 1)
    days_since_solstice_test(1, 2016, 12, 22, 1)
    days_since_solstice_test(71, 2016, 3, 1, 1)
    days_since_solstice_test(70, 2015, 3, 1, 1)
    days_since_solstice_test(365, 2016, 12, 20, 1)
    days_since_solstice_test(364, 2015, 12, 20, 1)

    days_since_solstice_test(0, 2015, 6, 21, -1)
    days_since_solstice_test(0, 2016, 6, 21, -1)
    days_since_solstice_test(364, 2015, 6, 20, -1)
    days_since_solstice_test(365, 2016, 6, 20, -1)

def test_PrayerTimes():
    date = DateComponents(2015, 7, 12)
    params = CalculationParameters()
    params.get_parameters_from_method(CalculationMethod.NORTH_AMERICA)

    params.madhab = Madhab.HANAFI
    coordinates = Coordinates(35.7750, -78.6336)
    prayer_times = PrayerTimes(coordinates, date, params)

    tz = ZoneInfo("America/New_York")

    assert prayer_times.fajr.astimezone(tz).strftime("%I:%M %p") == "04:42 AM"
    assert prayer_times.sunrise.astimezone(tz).strftime("%I:%M %p") == "06:08 AM"
    assert prayer_times.dhuhr.astimezone(tz).strftime("%I:%M %p") == "01:21 PM"
    assert prayer_times.asr.astimezone(tz).strftime("%I:%M %p") == "06:22 PM"
    assert prayer_times.maghrib.astimezone(tz).strftime("%I:%M %p") == "08:32 PM"
    assert prayer_times.isha.astimezone(tz).strftime("%I:%M %p") == "09:57 PM"


def days_since_solstice_test( value: int, year: int, month: int, day: int, latitude: float):
    """
    For Northern Hemisphere start from December 21
    (DYY=0 for December 21, and counting forward, DYY=11 for January 1 and so on).
    For Southern Hemisphere start from June 21
    (DYY=0 for June 21, and counting forward)
    """
    date = datetime(year, month, day)
    
    day_of_year = date.timetuple().tm_yday

    assert days_since_solstice(day_of_year, date.year, latitude) == value