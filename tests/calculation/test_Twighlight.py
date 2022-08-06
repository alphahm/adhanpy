from datetime import datetime
import pytest
from adhanpy.calculation.Twilight import days_since_solstice


@pytest.mark.parametrize(
    "year, month, day, latitude, expected",
    [
        (2016, 1, 1, 1, 11),
        (2015, 12, 31, 1, 10),
        (2016, 12, 31, 1, 10),
        (2016, 12, 21, 1, 0),
        (2016, 12, 22, 1, 1),
        (2016, 3, 1, 1, 71),
        (2015, 3, 1, 1, 70),
        (2016, 12, 20, 1, 365),
        (2015, 12, 20, 1, 364),
        (2015, 6, 21, -1, 0),
        (2016, 6, 21, -1, 0),
        (2015, 6, 20, -1, 364),
        (2016, 6, 20, -1, 365),
    ],
)
def test_days_since_solstice(year, month, day, latitude, expected):
    """
    For Northern Hemisphere start from December 21
    (DYY=0 for December 21, and counting forward, DYY=11 for January 1 and so on).
    For Southern Hemisphere start from June 21
    (DYY=0 for June 21, and counting forward)
    """

    # Arrange
    date = datetime(year, month, day)
    day_of_year = date.timetuple().tm_yday

    # Act, Assert
    assert days_since_solstice(day_of_year, date.year, latitude) == expected
