from adhanpy.calculation.CalculationMethod import CalculationMethod
from adhanpy.calculation.Madhab import Madhab
from adhanpy.calculation.HighLatitudeRule import HighLatitudeRule
from adhanpy.calculation.PrayerAdjustments import PrayerAdjustments
from adhanpy.data.NightPortions import NightPortions


class CalculationParameters:
    def __init__(
        self,
        method: CalculationMethod = None,
        adjustments: PrayerAdjustments = None,
        method_adjustments: PrayerAdjustments = None,
        isha_interval: int = 0,
        fajr_angle: float = 0.0,
        isha_angle: float = 0.0,
    ):
        # The madhab used to calculate Asr
        self.madhab = Madhab.SHAFI

        # Rules for placing bounds on Fajr and Isha for high latitude areas
        self.high_latitude_rule = HighLatitudeRule.MIDDLE_OF_THE_NIGHT

        # Minutes after Maghrib (if set, the time for Isha will be Maghrib plus isha_interval)
        self.isha_interval = isha_interval

        # angle for calculating fajr
        self.fajr_angle = fajr_angle

        # angle for calculating isha
        self.isha_angle = isha_angle

        # Used to optionally add or subtract a set amount of time from each prayer time
        self.adjustments = (
            adjustments if adjustments is not None else PrayerAdjustments()
        )

        # Used for method adjustments
        self.method_adjustments = (
            method_adjustments
            if method_adjustments is not None
            else PrayerAdjustments()
        )

        # The method used to do the calculation
        # method is last to be assigned, it has precedence and will overwrite some of the other parameters
        self.method = method

        if method is not None:
            self._set_parameters_using_method(method)
        else:
            self.method = CalculationMethod.OTHER

    def night_portions(self):
        if self.high_latitude_rule == HighLatitudeRule.MIDDLE_OF_THE_NIGHT:
            return NightPortions(1.0 / 2.0, 1.0 / 2.0)
        elif self.high_latitude_rule == HighLatitudeRule.SEVENTH_OF_THE_NIGHT:
            return NightPortions(1.0 / 7.0, 1.0 / 7.0)
        elif self.high_latitude_rule == HighLatitudeRule.TWILIGHT_ANGLE:
            return NightPortions(self.fajr_angle / 60.0, self.isha_angle / 60.0)
        else:
            raise ValueError("Invalid high latitude rule")

    def _set_parameters_using_method(self, calculation_method: CalculationMethod):
        # set parmeters given calculation method
        if calculation_method == CalculationMethod.MUSLIM_WORLD_LEAGUE:
            self.fajr_angle = 18.0
            self.isha_angle = 17.0
            self.method_adjustments = PrayerAdjustments(0, 0, 1, 0, 0, 0)

        elif calculation_method == CalculationMethod.EGYPTIAN:
            self.fajr_angle = 19.5
            self.isha_angle = 17.5
            self.method_adjustments = PrayerAdjustments(0, 0, 1, 0, 0, 0)

        elif calculation_method == CalculationMethod.KARACHI:
            self.fajr_angle = 18.0
            self.isha_angle = 18.0
            self.method_adjustments = PrayerAdjustments(0, 0, 1, 0, 0, 0)

        elif calculation_method == CalculationMethod.UMM_AL_QURA:
            self.fajr_angle = 18.5
            self.isha_interval = 90

        elif calculation_method == CalculationMethod.DUBAI:
            self.fajr_angle = 18.2
            self.isha_angle = 18.2
            self.method_adjustments = PrayerAdjustments(0, -3, 3, 3, 3, 0)

        elif calculation_method == CalculationMethod.MOON_SIGHTING_COMMITTEE:
            self.fajr_angle = 18.0
            self.isha_angle = 18.0
            self.method_adjustments = PrayerAdjustments(0, 0, 5, 0, 3, 0)

        elif calculation_method == CalculationMethod.NORTH_AMERICA:
            self.fajr_angle = 15.0
            self.isha_angle = 15.0
            self.method_adjustments = PrayerAdjustments(0, 0, 1, 0, 0, 0)

        elif calculation_method == CalculationMethod.KUWAIT:
            self.fajr_angle = 18.0
            self.isha_angle = 17.5

        elif calculation_method == CalculationMethod.QATAR:
            self.fajr_angle = 18.0
            self.isha_interval = 90

        elif calculation_method == CalculationMethod.SINGAPORE:
            self.fajr_angle = 20.0
            self.isha_angle = 18.0
            self.method_adjustments = PrayerAdjustments(0, 0, 1, 0, 0, 0)

        elif calculation_method == CalculationMethod.UOIF:
            self.fajr_angle = 12.0
            self.isha_angle = 12.0

        elif calculation_method == CalculationMethod.OTHER:
            self.fajr_angle = 0.0
            self.isha_angle = 0.0

        else:
            raise ValueError("Invalid CalculationMethod")
