class PrayerAdjustments:

    fajr: int
    # Fajr offset in minutes

    sunrise: int
    # Sunrise offset in minutes

    dhuhr: int
    # Dhuhr offset in minutes

    asr: int
    # Asr offset in minutes

    maghrib: int
    # Maghrib offset in minutes

    isha: int
    # Isha offset in minutes

    def __init__(
        self,
        fajr: int = 0,
        sunrise: int = 0,
        dhuhr: int = 0,
        asr: int = 0,
        maghrib: int = 0,
        isha: int = 0,
    ):
        """
        Gets a PrayerAdjustments object to offset prayer times (defaulting to 0)
        param fajr offset from fajr in minutes
        param sunrise offset from sunrise in minutes
        param dhuhr offset from dhuhr in minutes
        param asr offset from asr in minutes
        param maghrib offset from maghrib in minutes
        param isha offset from isha in minutes
        """
        self.fajr = fajr
        self.sunrise = sunrise
        self.dhuhr = dhuhr
        self.asr = asr
        self.maghrib = maghrib
        self.isha = isha
