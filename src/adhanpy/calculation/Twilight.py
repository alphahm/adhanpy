import calendar
from datetime import datetime, timedelta


def days_since_solstice(day_of_year: int, year: int, latitude: float) -> int:
    northern_offset = 10
    is_leap_year = calendar.isleap(year)

    southern_offset = 173 if is_leap_year else 172
    days_in_year = 366 if is_leap_year else 365

    if latitude >= 0:
        days_since_solstice = day_of_year + northern_offset
        if days_since_solstice >= days_in_year:
            days_since_solstice = days_since_solstice - days_in_year
    else:
        days_since_solstice = day_of_year - southern_offset
        if days_since_solstice < 0:
            days_since_solstice = days_since_solstice + days_in_year

    return days_since_solstice


def season_adjusted_morning_twilight(
    latitude: float, day_of_year: int, year: int, sunrise: datetime
):
    a = 75 + ((28.65 / 55.0) * abs(latitude))
    b = 75 + ((19.44 / 55.0) * abs(latitude))
    c = 75 + ((32.74 / 55.0) * abs(latitude))
    d = 75 + ((48.10 / 55.0) * abs(latitude))

    # final double adjustment;
    dyy = days_since_solstice(day_of_year, year, latitude)

    if dyy < 91:
        adjustment = a + (b - a) / 91.0 * dyy
    elif dyy < 137:
        adjustment = b + (c - b) / 46.0 * (dyy - 91)
    elif dyy < 183:
        adjustment = c + (d - c) / 46.0 * (dyy - 137)
    elif dyy < 229:
        adjustment = d + (c - d) / 46.0 * (dyy - 183)
    elif dyy < 275:
        adjustment = c + (b - c) / 46.0 * (dyy - 229)
    else:
        adjustment = b + (a - b) / 91.0 * (dyy - 275)

    return sunrise + timedelta(seconds=-int(round(adjustment * 60.0)))


def season_adjusted_evening_twilight(
    latitude: float, day: int, year: int, sunset: datetime
) -> datetime:
    a = 75 + ((25.60 / 55.0) * abs(latitude))
    b = 75 + ((2.050 / 55.0) * abs(latitude))
    c = 75 - ((9.210 / 55.0) * abs(latitude))
    d = 75 + ((6.140 / 55.0) * abs(latitude))

    dyy = days_since_solstice(day, year, latitude)
    if dyy < 91:
        adjustment = a + (b - a) / 91.0 * dyy
    elif dyy < 137:
        adjustment = b + (c - b) / 46.0 * (dyy - 91)
    elif dyy < 183:
        adjustment = c + (d - c) / 46.0 * (dyy - 137)
    elif dyy < 229:
        adjustment = d + (c - d) / 46.0 * (dyy - 183)
    elif dyy < 275:
        adjustment = c + (b - c) / 46.0 * (dyy - 229)
    else:
        adjustment = b + (a - b) / 91.0 * (dyy - 275)

    return sunset + timedelta(seconds=int(round(adjustment * 60.0)))
