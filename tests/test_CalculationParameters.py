import pytest
from adhanpy.CalculationMethod import CalculationMethod
from adhanpy.CalculationParameters import CalculationParameters
from adhanpy.HighLatitudeRule import HighLatitudeRule


def test_calculation_method():
    params = CalculationParameters(method=CalculationMethod.MUSLIM_WORLD_LEAGUE)
    assert params.fajr_angle == pytest.approx(18, abs=1e-6)
    assert params.isha_angle == pytest.approx(17, abs=1e-6)
    assert params.isha_interval == 0
    assert params.method == CalculationMethod.MUSLIM_WORLD_LEAGUE

    params = CalculationParameters(method=CalculationMethod.EGYPTIAN)
    assert params.fajr_angle == pytest.approx(19.5, abs=1e-6)
    assert params.isha_angle == pytest.approx(17.5, abs=1e-6)
    assert params.isha_interval == 0

    params = CalculationParameters(method=CalculationMethod.KARACHI)
    assert params.fajr_angle == pytest.approx(18, abs=1e-6)
    assert params.isha_angle == pytest.approx(18, abs=1e-6)
    assert params.isha_interval == 0

    params = CalculationParameters(method=CalculationMethod.UMM_AL_QURA)
    assert params.fajr_angle == pytest.approx(18.5, abs=1e-6)
    assert params.isha_angle == pytest.approx(0, abs=1e-6)
    assert params.isha_interval == 90

    params = CalculationParameters(method=CalculationMethod.DUBAI)
    assert params.fajr_angle == pytest.approx(18.2, abs=1e-6)
    assert params.isha_angle == pytest.approx(18.2, abs=1e-6)
    assert params.isha_interval == 0

    params = CalculationParameters(method=CalculationMethod.MOON_SIGHTING_COMMITTEE)
    assert params.fajr_angle == pytest.approx(18, abs=1e-6)
    assert params.isha_angle == pytest.approx(18, abs=1e-6)
    assert params.isha_interval == 0

    params = CalculationParameters(method=CalculationMethod.NORTH_AMERICA)
    assert params.fajr_angle == pytest.approx(15, abs=1e-6)
    assert params.isha_angle == pytest.approx(15, abs=1e-6)
    assert params.isha_interval == 0

    params = CalculationParameters(method=CalculationMethod.KUWAIT)
    assert params.fajr_angle == pytest.approx(18, abs=1e-6)
    assert params.isha_angle == pytest.approx(17.5, abs=1e-6)
    assert params.isha_interval == 0

    params = CalculationParameters(method=CalculationMethod.QATAR)
    assert params.fajr_angle == pytest.approx(18, abs=1e-6)
    assert params.isha_angle == pytest.approx(0, abs=1e-6)
    assert params.isha_interval == 90

    params = CalculationParameters(method=CalculationMethod.OTHER)
    assert params.fajr_angle == pytest.approx(0, abs=1e-6)
    assert params.isha_angle == pytest.approx(0, abs=1e-6)
    assert params.isha_interval == 0


def test_night_portion():
    parameters = CalculationParameters(fajr_angle=18, isha_angle=18)
    parameters.high_latitude_rule = HighLatitudeRule.MIDDLE_OF_THE_NIGHT

    assert parameters.night_portions().fajr == pytest.approx(0.5, abs=1e-3)
    assert parameters.night_portions().isha == pytest.approx(0.5, abs=1e-3)

    parameters = CalculationParameters(fajr_angle=18.0, isha_angle=18.0)
    parameters.high_latitude_rule = HighLatitudeRule.SEVENTH_OF_THE_NIGHT
    assert parameters.night_portions().fajr == pytest.approx(1.0 / 7.0, abs=1e-3)
    assert parameters.night_portions().isha == pytest.approx(1.0 / 7.0, abs=1e-3)

    parameters = CalculationParameters(fajr_angle=10.0, isha_angle=15.0)
    parameters.high_latitude_rule = HighLatitudeRule.TWILIGHT_ANGLE
    assert parameters.night_portions().fajr == pytest.approx(10.0 / 60.0, abs=1e-3)
    assert parameters.night_portions().isha == pytest.approx(15.0 / 60.0, abs=1e-3)
