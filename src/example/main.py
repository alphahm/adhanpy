from datetime import datetime
from zoneinfo import ZoneInfo
from adhanpy.calculation import CalculationMethod
from adhanpy.PrayerTimes import PrayerTimes


def print_prayer_times(prayer_times: PrayerTimes, time_zone: ZoneInfo):
    print(f"Prayer times for {today.astimezone(london_zone).strftime('%A %d %B %Y')}:")
    print(f"Fajr: {prayer_times.fajr.astimezone(london_zone).strftime('%H:%M')}")
    print(f"Sunrise: {prayer_times.sunrise.astimezone(london_zone).strftime('%H:%M')}")
    print(f"Dhuhr: {prayer_times.dhuhr.astimezone(london_zone).strftime('%H:%M')}")
    print(f"Asr: {prayer_times.asr.astimezone(london_zone).strftime('%H:%M')}")
    print(f"Maghrib: {prayer_times.maghrib.astimezone(london_zone).strftime('%H:%M')}")
    print(f"Isha: {prayer_times.isha.astimezone(london_zone).strftime('%H:%M')}")


if __name__ == "__main__":
    coordinates = (51.49799827422162, -0.1358135027951458)

    today = datetime.now()
    prayer_times = PrayerTimes(
        coordinates, today, CalculationMethod.MOON_SIGHTING_COMMITTEE
    )
    london_zone = ZoneInfo("Europe/London")

    print_prayer_times(prayer_times, london_zone)
