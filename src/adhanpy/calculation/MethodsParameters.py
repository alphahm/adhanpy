from adhanpy.calculation.CalculationMethod import CalculationMethod
from adhanpy.calculation.PrayerAdjustments import PrayerAdjustments


methods_parameters = {
    CalculationMethod.NONE: {},
    CalculationMethod.MUSLIM_WORLD_LEAGUE: {
        "fajr_angle": 18.0,
        "isha_angle": 17.0,
        "method_adjustments": PrayerAdjustments(dhuhr=1),
    },
    CalculationMethod.EGYPTIAN: {
        "fajr_angle": 19.5,
        "isha_angle": 17.5,
        "method_adjustments": PrayerAdjustments(dhuhr=1),
    },
    CalculationMethod.KARACHI: {
        "fajr_angle": 18.0,
        "isha_angle": 18.0,
        "method_adjustments": PrayerAdjustments(dhuhr=1),
    },
    CalculationMethod.UMM_AL_QURA: {"fajr_angle": 18.5, "isha_interval": 90},
    CalculationMethod.DUBAI: {
        "fajr_angle": 18.2,
        "isha_angle": 18.2,
        "method_adjustments": PrayerAdjustments(sunrise=-3, dhuhr=3, asr=3, maghrib=3),
    },
    CalculationMethod.MOON_SIGHTING_COMMITTEE: {
        "fajr_angle": 18.0,
        "isha_angle": 18.0,
        "method_adjustments": PrayerAdjustments(dhuhr=5, maghrib=3),
    },
    CalculationMethod.NORTH_AMERICA: {
        "fajr_angle": 15.0,
        "isha_angle": 15.0,
        "method_adjustments": PrayerAdjustments(dhuhr=1),
    },
    CalculationMethod.KUWAIT: {"fajr_angle": 18.0, "isha_angle": 17.5},
    CalculationMethod.QATAR: {"fajr_angle": 18.0, "isha_interval": 90},
    CalculationMethod.SINGAPORE: {
        "fajr_angle": 20.0,
        "isha_angle": 18.0,
        "method_adjustments": PrayerAdjustments(dhuhr=1),
    },
    CalculationMethod.UOIF: {"fajr_angle": 12.0, "isha_angle": 12.0},
}
