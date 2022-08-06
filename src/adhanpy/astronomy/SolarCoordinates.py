import math
from adhanpy.astronomy.CalendricalHelper import julian_century
from adhanpy.astronomy.Astronomical import (
    apparent_obliquity_of_the_ecliptic,
    apparent_solar_longitude,
    mean_obliquity_of_the_ecliptic,
    mean_sidereal_time,
    mean_solar_longitude,
    mean_lunar_longitude,
    ascending_lunar_node_longitude,
    nutation_in_longitude,
    nutation_in_obliquity,
)
from adhanpy.util.FloatUtil import unwind_angle


class SolarCoordinates:
    def __init__(self, julian_day) -> None:
        T = julian_century(julian_day)
        L0 = mean_solar_longitude(T)
        Lp = mean_lunar_longitude(T)
        Ω = ascending_lunar_node_longitude(T)
        λ = math.radians(apparent_solar_longitude(T, L0))
        θ0 = mean_sidereal_time(T)
        ΔΨ = nutation_in_longitude(T, L0, Lp, Ω)
        Δε = nutation_in_obliquity(T, L0, Lp, Ω)
        ε0 = mean_obliquity_of_the_ecliptic(T)
        εapp = math.radians(apparent_obliquity_of_the_ecliptic(T, ε0))

        # Equation from Astronomical Algorithms page 165
        self.declination = math.degrees(math.asin(math.sin(εapp) * math.sin(λ)))

        # Equation from Astronomical Algorithms page 165
        self.right_ascension = unwind_angle(
            math.degrees(math.atan2(math.cos(εapp) * math.sin(λ), math.cos(λ)))
        )

        # Equation from Astronomical Algorithms page 88
        self.apparent_sidereal_time = θ0 + (
            ((ΔΨ * 3600) * math.cos(math.radians(ε0 + Δε))) / 3600
        )
