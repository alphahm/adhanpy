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
    t = CalendricalHelper.julian_century(jd)

    l0 = Astronomical.mean_solar_longitude(t)
    epsilon0 = Astronomical.mean_obliquity_of_the_ecliptic(t)
    epsilon_app = Astronomical.apparent_obliquity_of_the_ecliptic(t, epsilon0)
    m = Astronomical.mean_solar_anomaly(t)
    c = Astronomical.solar_equation_of_the_center(t, m)
    iota = Astronomical.apparent_solar_longitude(t, l0)
    delta = solar.declination
    alpha = FloatUtil.unwind_angle(solar.right_ascension)

    assert t == pytest.approx(-0.072183436, abs=1e-11)
    assert l0 == pytest.approx(201.80720, abs=1e-5)
    assert epsilon0 == pytest.approx(23.44023, abs=1e-5)
    assert epsilon_app == pytest.approx(23.43999, abs=1e-5)
    assert m == pytest.approx(278.99397, abs=1e-5)
    assert c == pytest.approx(-1.89732, abs=1e-5)

    # lower accuracy than desired
    assert iota == pytest.approx(199.90895, abs=2e-5)
    assert delta == pytest.approx(-7.78507, abs=1e-5)
    assert alpha == pytest.approx(198.38083, abs=1e-5)

    # values from Astronomical Algorithms page 88
    jd = CalendricalHelper.julian_day(1987, 4, 10)
    solar = SolarCoordinates(jd)
    t = CalendricalHelper.julian_century(jd)

    theta0 = Astronomical.mean_sidereal_time(t)
    theta_app = solar.apparent_sidereal_time
    omega = Astronomical.ascending_lunar_node_longitude(t)
    epsilon0 = Astronomical.mean_obliquity_of_the_ecliptic(t)
    l0 = Astronomical.mean_solar_longitude(t)
    lp = Astronomical.mean_lunar_longitude(t)
    delta_psi = Astronomical.nutation_in_longitude(l0, lp, omega)
    delta_epsilon = Astronomical.nutation_in_obliquity(l0, lp, omega)
    epsilon = epsilon0 + delta_epsilon

    assert theta0 == pytest.approx(197.693195, abs=1e-6)
    assert theta_app == pytest.approx(197.6922295833, abs=1e-4)

    # values from Astronomical Algorithms page 148
    assert omega == pytest.approx(11.2531, abs=1e-4)
    assert delta_psi == pytest.approx(-0.0010522, abs=1e-4)
    assert delta_epsilon == pytest.approx(0.0026230556, abs=1e-5)
    assert epsilon0 == pytest.approx(23.4409463889, abs=1e-6)
    assert epsilon == pytest.approx(23.4435694444, abs=1e-5)


def test_altitude_of_celestial_body():
    phi = 38 + (55 / 60.0) + (17.0 / 3600)
    delta = -6 - (43 / 60.0) - (11.61 / 3600)
    h = 64.352133
    celestial_altitude = Astronomical.altitude_of_celestial_body(phi, delta, h)
    assert celestial_altitude == pytest.approx(15.1249, abs=1e-4)


def test_transit_and_hour_angle():
    # alues from Astronomical Algorithms page 103
    longitude = -71.0833
    theta = 177.74208
    alpha1 = 40.68021
    alpha2 = 41.73129
    alpha3 = 42.78204
    m0 = Astronomical.approximate_transit(longitude, theta, alpha2)

    assert m0 == pytest.approx(0.81965, abs=1e-5)

    transit = Astronomical.corrected_transit(m0, longitude, theta, alpha2, alpha1, alpha3) / 24

    assert transit == pytest.approx(0.81980, abs=1e-5)

    delta1 = 18.04761
    delta2 = 18.44092
    delta3 = 18.82742

    rise = (
        Astronomical.corrected_hour_angle(
            m0,
            -0.5667,
            Coordinates(42.3333, longitude),
            False,
            theta,
            alpha2,
            alpha1,
            alpha3,
            delta2,
            delta1,
            delta3,
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
