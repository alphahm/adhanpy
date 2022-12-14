import pytest
import adhanpy.util.FloatUtil as FloatUtil


@pytest.mark.parametrize(
    "value, max, expected, tolerance",
    [
        (2.0, -5, -3, 1e-5),
        (-4.0, -5.0, -4, 1e-5),
        (-6.0, -5.0, -1, 1e-5),
        (-1.0, 24, 23, 1e-5),
        (1.0, 24.0, 1, 1e-5),
        (49.0, 24, 1, 1e-5),
        (361.0, 360, 1, 1e-5),
        (360.0, 360, 0, 1e-5),
        (259.0, 360, 259, 1e-5),
        (2592.0, 360, 72, 1e-5),
        (360.1, 360, 0.1, 1e-2),
    ],
)
def test_normalize_with_bound(value, max, expected, tolerance):
    assert FloatUtil.normalize_with_bound(value, max) == pytest.approx(
        expected, abs=tolerance
    )


@pytest.mark.parametrize(
    "value, expected",
    [
        (-45.0, 315),
        (361.0, 1),
        (360.0, 0),
        (259.0, 259),
        (2592.0, 72),
    ],
)
def test_unwind_angle(value, expected):
    assert FloatUtil.unwind_angle(value) == pytest.approx(expected, abs=1e-5)


@pytest.mark.parametrize(
    "angle, expected, tolerance",
    [
        (360.0, 0, 1e-6),
        (361.0, 1, 1e-6),
        (1.0, 1, 1e-6),
        (-1.0, -1, 1e-6),
        (-181.0, 179, 1e-6),
        (180.0, 180, 1e-6),
        (359.0, -1, 1e-6),
        (-359.0, 1, 1e-6),
        (1261.0, -179, 1e-6),
        (-360.1, -0.1, 1e-2),
    ],
)
def test_closest_angle(angle, expected, tolerance):
    assert FloatUtil.closest_angle(angle) == pytest.approx(expected, abs=tolerance)
