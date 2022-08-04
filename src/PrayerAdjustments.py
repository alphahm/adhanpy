class PrayerAdjustments:

    """
    Fajr offset in minutes
    """
    fajr: int

    """
    Sunrise offset in minutes
    """
    sunrise: int

    """
    Dhuhr offset in minutes
    """
    dhuhr: int

    """
    Asr offset in minutes
    """
    asr: int

    """
    Maghrib offset in minutes
    """
    maghrib: int

    """
    Isha offset in minutes
    """
    isha: int

    """
    Gets a PrayerAdjustments object to offset prayer times (defaulting to 0)
    param fajr offset from fajr in minutes
    param sunrise offset from sunrise in minutes
    param dhuhr offset from dhuhr in minutes
    param asr offset from asr in minutes
    param maghrib offset from maghrib in minutes
    param isha offset from isha in minutes
    """
    def __init__(self, fajr: int = 0, sunrise: int = 0, dhuhr: int = 0, asr: int = 0, maghrib: int = 0, isha: int = 0):
        self.fajr = fajr
        self.sunrise = sunrise
        self.dhuhr = dhuhr
        self.asr = asr
        self.maghrib = maghrib
        self.isha = isha
