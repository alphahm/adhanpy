from enum import Enum


class CalculationMethod(Enum):

    MUSLIM_WORLD_LEAGUE = 0
    """
    Muslim World League
    Uses Fajr angle of 18 and an Isha angle of 17
    """

    EGYPTIAN = 1
    """
    Egyptian General Authority of Survey
    Uses Fajr angle of 19.5 and an Isha angle of 17.5
    """

    KARACHI = 2
    """
    University of Islamic Sciences, Karachi
    Uses Fajr angle of 18 and an Isha angle of 18
    """

    UMM_AL_QURA = 3
    """
    Umm al-Qura University, Makkah
    Uses a Fajr angle of 18.5 and an Isha angle of 90. Note: You should add a +30 minute custom
    adjustment of Isha during Ramadan.
    """

    DUBAI = 4
    """
    The Gulf Region
    Uses Fajr and Isha angles of 18.2 degrees.
    """

    MOON_SIGHTING_COMMITTEE = 5
    """
    Moonsighting Committee
    Uses a Fajr angle of 18 and an Isha angle of 18. Also uses seasonal adjustment values.
    """

    NORTH_AMERICA = 6
    """
    Referred to as the ISNA method
    This method is included for completeness, but is not recommended.
    Uses a Fajr angle of 15 and an Isha angle of 15.
    """

    KUWAIT = 7
    """
    Kuwait
    Uses a Fajr angle of 18 and an Isha angle of 17.5
    """

    QATAR = 8
    """
    Qatar
    Modified version of Umm al-Qura that uses a Fajr angle of 18.
    """

    SINGAPORE = 9
    """
    Singapore
    Uses a Fajr angle of 20 and an Isha angle of 18
    """

    UOIF = 10
    """
    UOIF
    Uses a Fajr angle of 12 and an Isha angle of 12
    """

    OTHER = 11
    """
    The default value for CalculationParameters.method when initializing a
    CalculationParameters object. Sets a Fajr angle of 0 and an Isha angle of 0.
    """
