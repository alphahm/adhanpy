from adhanpy.data.Coordinates import Coordinates
from adhanpy.util.FloatUtil import closest_angle, unwind_angle, normalize_with_bound
import math


def mean_solar_longitude(T: float) -> float:
    # Equation from Astronomical Algorithms page 163
    term1 = 280.4664567
    term2 = 36000.76983 * T
    term3 = 0.0003032 * (T**2)
    L0 = term1 + term2 + term3
    return unwind_angle(L0)


def mean_lunar_longitude(T: float) -> float:
    # Equation from Astronomical Algorithms page 144
    term1 = 218.3165
    term2 = 481267.8813 * T
    Lp = term1 + term2
    return unwind_angle(Lp)


def ascending_lunar_node_longitude(T: float) -> float:
    # Equation from Astronomical Algorithms page 144
    term1 = 125.04452
    term2 = 1934.136261 * T
    term3 = 0.0020708 * (T**2)
    term4 = (T**3) / 450000
    Ω = term1 - term2 + term3 + term4
    return unwind_angle(Ω)


def apparent_solar_longitude(T: float, L0: float) -> float:
    longitude = L0 + solar_equation_of_the_center(T, mean_solar_anomaly(T))
    Ω = 125.04 - (1934.136 * T)
    λ = longitude - 0.00569 - (0.00478 * math.sin(math.radians(Ω)))
    return unwind_angle(λ)


def solar_equation_of_the_center(T: float, M: float) -> float:
    # Equation from Astronomical Algorithms page 164
    Mrad = math.radians(M)
    term1 = (1.914602 - (0.004817 * T) - (0.000014 * (T**2))) * math.sin(Mrad)
    term2 = (0.019993 - (0.000101 * T)) * math.sin(2 * Mrad)
    term3 = 0.000289 * math.sin(3 * Mrad)
    return term1 + term2 + term3


def mean_solar_anomaly(T: float) -> float:
    # Equation from Astronomical Algorithms page 163
    term1 = 357.52911
    term2 = 35999.05029 * T
    term3 = 0.0001537 * (T**2)
    M = term1 + term2 - term3
    return unwind_angle(M)


def mean_sidereal_time(T: float) -> float:
    # Equation from Astronomical Algorithms page 165
    JD = (T * 36525) + 2451545.0
    term1 = 280.46061837
    term2 = 360.98564736629 * (JD - 2451545)
    term3 = 0.000387933 * (T**2)
    term4 = (T**3) / 38710000
    θ = term1 + term2 + term3 - term4
    return unwind_angle(θ)


def nutation_in_longitude(L0: float, Lp: float, Ω: float) -> float:
    # Equation from Astronomical Algorithms page 144
    term1 = (-17.2 / 3600) * math.sin(math.radians(Ω))
    term2 = (1.32 / 3600) * math.sin(2 * math.radians(L0))
    term3 = (0.23 / 3600) * math.sin(2 * math.radians(Lp))
    term4 = (0.21 / 3600) * math.sin(2 * math.radians(Ω))
    return term1 - term2 - term3 + term4


def nutation_in_obliquity(L0: float, Lp: float, Ω: float) -> float:
    # Equation from Astronomical Algorithms page 144
    term1 = (9.2 / 3600) * math.cos(math.radians(Ω))
    term2 = (0.57 / 3600) * math.cos(2 * math.radians(L0))
    term3 = (0.10 / 3600) * math.cos(2 * math.radians(Lp))
    term4 = (0.09 / 3600) * math.cos(2 * math.radians(Ω))
    return term1 + term2 + term3 - term4


def mean_obliquity_of_the_ecliptic(T: float) -> float:
    # Equation from Astronomical Algorithms page 147
    term1 = 23.439291
    term2 = 0.013004167 * T
    term3 = 0.0000001639 * (T**2)
    term4 = 0.0000005036 * (T**3)
    return term1 - term2 - term3 + term4


def apparent_obliquity_of_the_ecliptic(T: float, ε0: float) -> float:
    # Equation from Astronomical Algorithms page 165
    O = 125.04 - (1934.136 * T)
    return ε0 + (0.00256 * math.cos(math.radians(O)))


def altitude_of_celestial_body(φ: float, δ: float, H: float) -> float:
    # Equation from Astronomical Algorithms page 93
    term1 = math.sin(math.radians(φ)) * math.sin(math.radians(δ))
    term2 = (
        math.cos(math.radians(φ))
        * math.cos(math.radians(δ))
        * math.cos(math.radians(H))
    )
    return math.degrees(math.asin(term1 + term2))


def approximate_transit(L: float, Θ0: float, α2: float) -> float:
    # Equation from page Astronomical Algorithms 102
    Lw = L * -1
    return normalize_with_bound((α2 + Lw - Θ0) / 360, 1)


def corrected_transit(
    m0: float, L: float, Θ0: float, α2: float, α1: float, α3: float
) -> float:
    # Equation from page Astronomical Algorithms 102
    Lw = L * -1
    θ = unwind_angle(Θ0 + (360.985647 * m0))
    α = unwind_angle(interpolate_angles(α2, α1, α3, m0))
    H = closest_angle(θ - Lw - α)
    Δm = H / -360
    return (m0 + Δm) * 24


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
    Θ0: float,
    α2: float,
    α1: float,
    α3: float,
    δ2: float,
    δ1: float,
    δ3: float,
) -> float:
    # Equation from page Astronomical Algorithms 102
    Lw = coordinates.longitude * -1
    term1 = math.sin(math.radians(h0)) - (
        math.sin(math.radians(coordinates.latitude)) * math.sin(math.radians(δ2))
    )
    term2 = math.cos(math.radians(coordinates.latitude)) * math.cos(math.radians(δ2))
    try:
        H0 = math.degrees(math.acos(term1 / term2))
        m = m0 + (H0 / 360) if afterTransit else m0 - (H0 / 360)
        θ = unwind_angle(Θ0 + (360.985647 * m))
        α = unwind_angle(interpolate_angles(α2, α1, α3, m))
        δ = interpolate(δ2, δ1, δ3, m)
        H = θ - Lw - α
        h = altitude_of_celestial_body(coordinates.latitude, δ, H)
        term3 = h - h0
        term4 = (
            360
            * math.cos(math.radians(δ))
            * math.cos(math.radians(coordinates.latitude))
            * math.sin(math.radians(H))
        )
        Δm = term3 / term4
    except:
        return math.nan

    return (m + Δm) * 24
