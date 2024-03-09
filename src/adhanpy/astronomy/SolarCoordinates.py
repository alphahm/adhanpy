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
        jc = julian_century(julian_day)
        mean_solar_long = mean_solar_longitude(jc)
        mean_lunar_long = mean_lunar_longitude(jc)
        omega = ascending_lunar_node_longitude(jc)
        iota = math.radians(apparent_solar_longitude(jc, mean_solar_long))
        theta_0 = mean_sidereal_time(jc)
        delta_psi = nutation_in_longitude(mean_solar_long, mean_lunar_long, omega)
        delta_epsilon = nutation_in_obliquity(mean_solar_long, mean_lunar_long, omega)
        epsilon_0 = mean_obliquity_of_the_ecliptic(jc)
        epsilon_app = math.radians(apparent_obliquity_of_the_ecliptic(jc, epsilon_0))

        # Equation from Astronomical Algorithms page 165
        self.declination = math.degrees(
            math.asin(math.sin(epsilon_app) * math.sin(iota))
        )

        # Equation from Astronomical Algorithms page 165
        self.right_ascension = unwind_angle(
            math.degrees(
                math.atan2(math.cos(epsilon_app) * math.sin(iota), math.cos(iota))
            )
        )

        # Equation from Astronomical Algorithms page 88
        self.apparent_sidereal_time = theta_0 + (
            ((delta_psi * 3600) * math.cos(math.radians(epsilon_0 + delta_epsilon)))
            / 3600
        )
