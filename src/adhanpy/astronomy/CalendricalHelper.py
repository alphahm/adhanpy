import math


def julian_day(
    year: int, month: int, day: int, hours: float = 0.0, minutes: float = 0.0
):
    if minutes != 0.0:
        hours = hours + (minutes / 60.0)

    y = year if month > 2 else year - 1
    m = month if month > 2 else month + 12
    d = day + (hours / 24)

    a = math.floor(y / 100)
    b = math.floor(2 - a + (a / 4))

    i0 = int(365.25 * (y + 4716))
    i1 = int(30.6001 * (m + 1))

    return i0 + i1 + d + b - 1524.5


def julian_century(j_day):
    # Equation from Astronomical Algorithms page 163
    return (j_day - 2451545.0) / 36525
