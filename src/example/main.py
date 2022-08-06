from datetime import datetime
from zoneinfo import ZoneInfo
from adhanpy.calculation import CalculationMethod
from adhanpy.PrayerTimes import PrayerTimes


def print_prayer_times(when: datetime, prayer_times: PrayerTimes):
    format = "%H:%M"
    print(f"Prayer times for {today.strftime('%A %d %B %Y')}:")
    print(f"Fajr: {prayer_times.fajr.strftime(format)}")
    print(f"Sunrise: {prayer_times.sunrise.strftime(format)}")
    print(f"Dhuhr: {prayer_times.dhuhr.strftime(format)}")
    print(f"Asr: {prayer_times.asr.strftime(format)}")
    print(f"Maghrib: {prayer_times.maghrib.strftime(format)}")
    print(f"Isha: {prayer_times.isha.strftime(format)}")


if __name__ == "__main__":
    coordinates = (51.49799827422162, -0.1358135027951458)

    today = datetime.now()
    london_zone = ZoneInfo("Europe/London")
    prayer_times = PrayerTimes(
        coordinates,
        today,
        CalculationMethod.MOON_SIGHTING_COMMITTEE,
        time_zone=london_zone,
    )

    print_prayer_times(today, prayer_times)
