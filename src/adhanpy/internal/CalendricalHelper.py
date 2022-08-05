import math


def julian_day(
    year: int, month: int, day: int, hours: float = 0.0, minutes: float = 0.0
):
    if minutes != 0.0:
        hours = hours + (minutes / 60.0)

    Y = year if month > 2 else year - 1
    M = month if month > 2 else month + 12
    D = day + (hours / 24)

    A = math.floor(Y / 100)
    B = math.floor(2 - A + (A / 4))

    i0 = int(365.25 * (Y + 4716))
    i1 = int(30.6001 * (M + 1))

    return i0 + i1 + D + B - 1524.5


def julian_century(JD):
    # Equation from Astronomical Algorithms page 163
    return (JD - 2451545.0) / 36525
