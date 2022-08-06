import pytest
import adhanpy.astronomy.Astronomical as Astronomical
import adhanpy.util.FloatUtil as FloatUtil
import adhanpy.astronomy.CalendricalHelper as CalendricalHelper
from adhanpy.astronomy.SolarCoordinates import SolarCoordinates
from adhanpy.data.Coordinates import Coordinates


def test_solar_coordinates():

    # values from Astronomical Algorithms page 165
    jd = CalendricalHelper.julian_day(1992, 10, 13)
    solar = SolarCoordinates(jd)
    T = CalendricalHelper.julian_century(jd)

    L0 = Astronomical.mean_solar_longitude(T)
    ε0 = Astronomical.mean_obliquity_of_the_ecliptic(T)
    εapp = Astronomical.apparent_obliquity_of_the_ecliptic(T, ε0)
    M = Astronomical.mean_solar_anomaly(T)
    C = Astronomical.solar_equation_of_the_center(T, M)
    λ = Astronomical.apparent_solar_longitude(T, L0)
    δ = solar.declination
    α = FloatUtil.unwind_angle(solar.right_ascension)

    assert T == pytest.approx(-0.072183436, abs=1e-11)
    assert L0 == pytest.approx(201.80720, abs=1e-5)
    assert ε0 == pytest.approx(23.44023, abs=1e-5)
    assert εapp == pytest.approx(23.43999, abs=1e-5)
    assert M == pytest.approx(278.99397, abs=1e-5)
    assert C == pytest.approx(-1.89732, abs=1e-5)

    # lower accuracy than desired
    assert λ == pytest.approx(199.90895, abs=2e-5)
    assert δ == pytest.approx(-7.78507, abs=1e-5)
    assert α == pytest.approx(198.38083, abs=1e-5)

    # values from Astronomical Algorithms page 88
    jd = CalendricalHelper.julian_day(1987, 4, 10)
    solar = SolarCoordinates(jd)
    T = CalendricalHelper.julian_century(jd)

    θ0 = Astronomical.mean_sidereal_time(T)
    θapp = solar.apparent_sidereal_time
    Ω = Astronomical.ascending_lunar_node_longitude(T)
    ε0 = Astronomical.mean_obliquity_of_the_ecliptic(T)
    L0 = Astronomical.mean_solar_longitude(T)
    Lp = Astronomical.mean_lunar_longitude(T)
    ΔΨ = Astronomical.nutation_in_longitude(T, L0, Lp, Ω)
    Δε = Astronomical.nutation_in_obliquity(T, L0, Lp, Ω)
    ε = ε0 + Δε

    assert θ0 == pytest.approx(197.693195, abs=1e-6)
    assert θapp == pytest.approx(197.6922295833, abs=1e-4)

    # values from Astronomical Algorithms page 148
    assert Ω == pytest.approx(11.2531, abs=1e-4)
    assert ΔΨ == pytest.approx(-0.0010522, abs=1e-4)
    assert Δε == pytest.approx(0.0026230556, abs=1e-5)
    assert ε0 == pytest.approx(23.4409463889, abs=1e-6)
    assert ε == pytest.approx(23.4435694444, abs=1e-5)


def test_altitude_of_celestial_body():
    φ = 38 + (55 / 60.0) + (17.0 / 3600)
    δ = -6 - (43 / 60.0) - (11.61 / 3600)
    H = 64.352133
    h = Astronomical.altitude_of_celestial_body(φ, δ, H)
    assert h == pytest.approx(15.1249, abs=1e-4)


def test_transit_and_hour_angle():
    # alues from Astronomical Algorithms page 103
    longitude = -71.0833
    Θ = 177.74208
    α1 = 40.68021
    α2 = 41.73129
    α3 = 42.78204
    m0 = Astronomical.approximate_transit(longitude, Θ, α2)

    assert m0 == pytest.approx(0.81965, abs=1e-5)

    transit = Astronomical.corrected_transit(m0, longitude, Θ, α2, α1, α3) / 24

    assert transit == pytest.approx(0.81980, abs=1e-5)

    δ1 = 18.04761
    δ2 = 18.44092
    δ3 = 18.82742

    rise = (
        Astronomical.corrected_hour_angle(
            m0,
            -0.5667,
            Coordinates(42.3333, longitude),
            False,
            Θ,
            α2,
            α1,
            α3,
            δ2,
            δ1,
            δ3,
        )
        / 24
    )
    assert rise == pytest.approx(0.51766, abs=1e-5)


def test_interpolation():
    # values from Astronomical Algorithms page 25
    interpolated_value_1 = Astronomical.interpolate(
        0.877366, 0.884226, 0.870531, 4.35 / 24
    )
    interpolated_value_2 = Astronomical.interpolate(1, -1, 3, 0.6)

    assert interpolated_value_1 == pytest.approx(0.876125, abs=1e-6)
    assert interpolated_value_2 == pytest.approx(2.2, abs=1e-6)


def test_angle_interpolation():
    i1 = Astronomical.interpolate_angles(1, -1, 3, 0.6)
    assert i1 == pytest.approx(2.2, abs=1e-6)

    i2 = Astronomical.interpolate_angles(1, 359, 3, 0.6)
    assert i2 == pytest.approx(2.2, abs=1e-6)
