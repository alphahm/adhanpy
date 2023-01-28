from typing import Optional
from adhanpy.calculation.CalculationMethod import CalculationMethod
from adhanpy.calculation.MethodsParameters import methods_parameters
from adhanpy.calculation.Madhab import Madhab
from adhanpy.calculation.HighLatitudeRule import HighLatitudeRule
from adhanpy.calculation.PrayerAdjustments import PrayerAdjustments
from adhanpy.data.NightPortions import NightPortions


class CalculationParameters:
    def __init__(
        self,
        method: Optional[CalculationMethod] = None,
        adjustments: Optional[PrayerAdjustments] = None,
        method_adjustments: Optional[PrayerAdjustments] = None,
        isha_interval: int = 0,
        fajr_angle: float = 0.0,
        isha_angle: float = 0.0,
    ) -> None:
        # The madhab used to calculate Asr
        self.madhab = Madhab.SHAFI

        # Rules for placing bounds on Fajr and Isha for high latitude areas
        self.high_latitude_rule = HighLatitudeRule.MIDDLE_OF_THE_NIGHT

        # Minutes after Maghrib (if set, the time for Isha will be Maghrib plus isha_interval)
        self.isha_interval = isha_interval

        # fajr and isha angles
        self.fajr_angle = fajr_angle
        self.isha_angle = isha_angle

        # Used to optionally add or subtract a set amount of time from each prayer time
        self.adjustments = (
            adjustments if adjustments is not None else PrayerAdjustments()
        )

        # method is last assigned and has precedence and will overwrite other parameters
        self.method = (
            method if isinstance(method, CalculationMethod) else CalculationMethod.NONE
        )

        # Used for method adjustments
        self.method_adjustments = (
            method_adjustments
            if method_adjustments is not None
            else PrayerAdjustments()
        )

        self._set_parameters_using_method()

    def night_portions(self) -> NightPortions:
        if self.high_latitude_rule == HighLatitudeRule.MIDDLE_OF_THE_NIGHT:
            return NightPortions(1.0 / 2.0, 1.0 / 2.0)

        elif self.high_latitude_rule == HighLatitudeRule.SEVENTH_OF_THE_NIGHT:
            return NightPortions(1.0 / 7.0, 1.0 / 7.0)

        elif self.high_latitude_rule == HighLatitudeRule.TWILIGHT_ANGLE:
            return NightPortions(self.fajr_angle / 60.0, self.isha_angle / 60.0)

        raise ValueError("Invalid high latitude rule")

    def _set_parameters_using_method(self) -> None:
        method_parameters = methods_parameters[self.method]
        for key, value in method_parameters.items():
            setattr(self, key, value)
