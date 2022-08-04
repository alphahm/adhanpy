def julian_day(year, month, day, hours):
    Y = year if month > 2 else year - 1
    M = month if month > 2 else month + 12
    D = day + (hours / 24)

    A = int(Y / 100)
    B = int(2 - A + (A / 4))

    i0 = int(365.25 * (Y + 4716))
    i1 = int(30.6001 * (M + 1))

    return i0 + i1 + D + B - 1524.5

def julian_century(JD):
    # Equation from Astronomical Algorithms page 163
    return (JD - 2451545.0) / 36525
