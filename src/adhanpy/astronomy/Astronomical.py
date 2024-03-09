from adhanpy.data.Coordinates import Coordinates
from adhanpy.util.FloatUtil import closest_angle, unwind_angle, normalize_with_bound
import math


def mean_solar_longitude(t: float) -> float:
    # Equation from Astronomical Algorithms page 163
    term1 = 280.4664567
    term2 = 36000.76983 * t
    term3 = 0.0003032 * (t**2)
    l_0 = term1 + term2 + term3
    return unwind_angle(l_0)


def mean_lunar_longitude(t: float) -> float:
    # Equation from Astronomical Algorithms page 144
    term1 = 218.3165
    term2 = 481267.8813 * t
    l_p = term1 + term2
    return unwind_angle(l_p)


def ascending_lunar_node_longitude(t: float) -> float:
    # Equation from Astronomical Algorithms page 144
    term1 = 125.04452
    term2 = 1934.136261 * t
    term3 = 0.0020708 * (t**2)
    term4 = (t**3) / 450000
    omega = term1 - term2 + term3 + term4
    return unwind_angle(omega)


def apparent_solar_longitude(t: float, l_0: float) -> float:
    longitude = l_0 + solar_equation_of_the_center(t, mean_solar_anomaly(t))
    omega = 125.04 - (1934.136 * t)
    iota = longitude - 0.00569 - (0.00478 * math.sin(math.radians(omega)))
    return unwind_angle(iota)


def solar_equation_of_the_center(t: float, m: float) -> float:
    # Equation from Astronomical Algorithms page 164
    m_rad = math.radians(m)
    term1 = (1.914602 - (0.004817 * t) - (0.000014 * (t**2))) * math.sin(m_rad)
    term2 = (0.019993 - (0.000101 * t)) * math.sin(2 * m_rad)
    term3 = 0.000289 * math.sin(3 * m_rad)
    return term1 + term2 + term3


def mean_solar_anomaly(t: float) -> float:
    # Equation from Astronomical Algorithms page 163
    term1 = 357.52911
    term2 = 35999.05029 * t
    term3 = 0.0001537 * (t**2)
    m = term1 + term2 - term3
    return unwind_angle(m)


def mean_sidereal_time(t: float) -> float:
    # Equation from Astronomical Algorithms page 165
    jd = (t * 36525) + 2451545.0
    term1 = 280.46061837
    term2 = 360.98564736629 * (jd - 2451545)
    term3 = 0.000387933 * (t**2)
    term4 = (t**3) / 38710000
    theta = term1 + term2 + term3 - term4
    return unwind_angle(theta)


def nutation_in_longitude(l_0: float, lp: float, omega: float) -> float:
    # Equation from Astronomical Algorithms page 144
    term1 = (-17.2 / 3600) * math.sin(math.radians(omega))
    term2 = (1.32 / 3600) * math.sin(2 * math.radians(l_0))
    term3 = (0.23 / 3600) * math.sin(2 * math.radians(lp))
    term4 = (0.21 / 3600) * math.sin(2 * math.radians(omega))
    return term1 - term2 - term3 + term4


def nutation_in_obliquity(l_0: float, l_p: float, omega: float) -> float:
    # Equation from Astronomical Algorithms page 144
    term1 = (9.2 / 3600) * math.cos(math.radians(omega))
    term2 = (0.57 / 3600) * math.cos(2 * math.radians(l_0))
    term3 = (0.10 / 3600) * math.cos(2 * math.radians(l_p))
    term4 = (0.09 / 3600) * math.cos(2 * math.radians(omega))
    return term1 + term2 + term3 - term4


def mean_obliquity_of_the_ecliptic(t: float) -> float:
    # Equation from Astronomical Algorithms page 147
    term1 = 23.439291
    term2 = 0.013004167 * t
    term3 = 0.0000001639 * (t**2)
    term4 = 0.0000005036 * (t**3)
    return term1 - term2 - term3 + term4


def apparent_obliquity_of_the_ecliptic(t: float, epsilon_0: float) -> float:
    # Equation from Astronomical Algorithms page 165
    O = 125.04 - (1934.136 * t)
    return epsilon_0 + (0.00256 * math.cos(math.radians(O)))


def altitude_of_celestial_body(phi: float, delta: float, h: float) -> float:
    # Equation from Astronomical Algorithms page 93
    term1 = math.sin(math.radians(phi)) * math.sin(math.radians(delta))
    term2 = (
        math.cos(math.radians(phi))
        * math.cos(math.radians(delta))
        * math.cos(math.radians(h))
    )
    return math.degrees(math.asin(term1 + term2))


def approximate_transit(l: float, theta_0: float, alpha_2: float) -> float:
    # Equation from page Astronomical Algorithms 102
    lw = l * -1
    return normalize_with_bound((alpha_2 + lw - theta_0) / 360, 1)


def corrected_transit(
    m0: float, l: float, theta_0: float, alpha_2: float, alpha_1: float, alpha_3: float
) -> float:
    # Equation from page Astronomical Algorithms 102
    lw = l * -1
    theta = unwind_angle(theta_0 + (360.985647 * m0))
    alpha = unwind_angle(interpolate_angles(alpha_2, alpha_1, alpha_3, m0))
    h = closest_angle(theta - lw - alpha)
    delta_m = h / -360
    return (m0 + delta_m) * 24


def interpolate(y2: float, y1: float, y3: float, n: float) -> float:
    # Equation from Astronomical Algorithms page 24
    a = y2 - y1
    b = y3 - y2
    c = b - a
    return y2 + ((n / 2) * (a + b + (n * c)))


def interpolate_angles(y2: float, y1: float, y3: float, n: float) -> float:
    # Equation from Astronomical Algorithms page 24
    a = unwind_angle(y2 - y1)
    b = unwind_angle(y3 - y2)
    c = b - a
    return y2 + ((n / 2) * (a + b + (n * c)))


def corrected_hour_angle(
    m0: float,
    h0: float,
    coordinates: Coordinates,
    afterTransit: bool,
    theta_0: float,
    alpha_2: float,
    alpha_1: float,
    alpha_3: float,
    delta_2: float,
    delta_1: float,
    delta_3: float,
) -> float:
    # Equation from page Astronomical Algorithms 102
    Lw = coordinates.longitude * -1
    term1 = math.sin(math.radians(h0)) - (
        math.sin(math.radians(coordinates.latitude)) * math.sin(math.radians(delta_2))
    )
    term2 = math.cos(math.radians(coordinates.latitude)) * math.cos(
        math.radians(delta_2)
    )
    try:
        h_0 = math.degrees(math.acos(term1 / term2))
        m = m0 + (h_0 / 360) if afterTransit else m0 - (h_0 / 360)
        theta = unwind_angle(theta_0 + (360.985647 * m))
        alpha = unwind_angle(interpolate_angles(alpha_2, alpha_1, alpha_3, m))
        delta = interpolate(delta_2, delta_1, delta_3, m)
        h = theta - Lw - alpha
        celestial_altitude = altitude_of_celestial_body(coordinates.latitude, delta, h)
        term3 = celestial_altitude - h0
        term4 = (
            360
            * math.cos(math.radians(delta))
            * math.cos(math.radians(coordinates.latitude))
            * math.sin(math.radians(h))
        )
        delta_m = term3 / term4
    except:
        return math.nan

    return (m + delta_m) * 24
