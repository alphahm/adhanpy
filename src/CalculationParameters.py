from CalculationMethod import CalculationMethod
from Madhab import Madhab
from HighLatitudeRule import HighLatitudeRule
from PrayerAdjustments import PrayerAdjustments
from NightPortions import NightPortions


class CalculationParameters:

    method = CalculationMethod.OTHER
    # The method used to do the calculation

    fajr_angle: float
    # The angle of the sun used to calculate fajr

    isha_angle: float
    # The angle of the sun used to calculate isha

    isha_interval: int
    # Minutes after Maghrib (if set, the time for Isha will be Maghrib plus isha_interval)

    madhab = Madhab.SHAFI
    # The madhab used to calculate Asr

    highLatitudeRule = HighLatitudeRule.MIDDLE_OF_THE_NIGHT
    # Rules for placing bounds on Fajr and Isha for high latitude areas

    adjustments = PrayerAdjustments()
    # Used to optionally add or subtract a set amount of time from each prayer time

    method_adjustments = PrayerAdjustments()
    # Used for method adjustments

    def from_angles(self, fajr_angle: float, isha_angle: float):
        """
        Generate CalculationParameters from angles
        param fajr_angle the angle for calculating fajr
        param isha_angle the angle for calculating isha
        """
        self.fajr_angle = fajr_angle
        self.isha_angle = isha_angle
        return self

    def from_fajr_angle_and_isha_interval(self, fajr_angle: float, isha_interval: int):
        """
        Generate CalculationParameters from fajr angle and isha interval
        param fajr_angle the angle for calculating fajr
        param isha_interval the amount of time after maghrib to have isha
        """
        self.from_angles(fajr_angle, 0.0)
        self.isha_interval = isha_interval
        return self

    def from_angles_and_calculation_method(
        self,
        fajr_angle: float,
        isha_angle: float,
        calculation_method: CalculationMethod,
    ):
        """
        Generate CalculationParameters from angles and a calculation method
        param fajr_angle the angle for calculating fajr
        param isha_angle the angle for calculating isha
        param method the calculation method to use
        """
        self.from_angles(fajr_angle, isha_angle)
        self.method = calculation_method
        return self

    def from_fajr_angle_isha_interval_and_calculation_method(
        self,
        fajr_angle: float,
        isha_interval: int,
        calculation_method: CalculationMethod,
    ):
        """
        Generate CalculationParameters from fajr angle, isha interval, and calculation method
        param fajr_angle the angle for calculating fajr
        param isha_interval the amount of time after maghrib to have isha
        param method the calculation method to use
        """
        self.from_fajr_angle_and_isha_interval(fajr_angle, isha_interval)
        self.method = calculation_method
        return self

    def with_method_adjustments(self, prayer_adjustments: PrayerAdjustments):
        """
        Set the method adjustments for the current calculation parameters
        param adjustments the prayer adjustments
        return this calculation parameters instance
        """
        self.method_adjustments = prayer_adjustments
        return self

    def night_portions(self):
        if self.highLatitudeRule == HighLatitudeRule.MIDDLE_OF_THE_NIGHT:
            return NightPortions(1.0 / 2.0, 1.0 / 2.0)
        elif self.highLatitudeRule == HighLatitudeRule.SEVENTH_OF_THE_NIGHT:
            return NightPortions(1.0 / 7.0, 1.0 / 7.0)
        elif self.highLatitudeRule == HighLatitudeRule.TWILIGHT_ANGLE:
            return NightPortions(self.fajr_angle / 60.0, self.isha_angle / 60.0)
        else:
            raise ValueError("Invalid high latitude rule")

    def get_parameters_from_method(self, calculation_method: CalculationMethod):
        """
        Return the CalculationParameters for the given method
        return CalculationParameters for the given Calculation method
        """
        if calculation_method == CalculationMethod.MUSLIM_WORLD_LEAGUE:
            return self.from_angles_and_calculation_method(
                18.0, 17.0, calculation_method
            ).with_method_adjustments(PrayerAdjustments(0, 0, 1, 0, 0, 0))

        elif calculation_method == CalculationMethod.EGYPTIAN:
            return self.from_angles_and_calculation_method(
                19.5, 17.5, calculation_method
            ).with_method_adjustments(PrayerAdjustments(0, 0, 1, 0, 0, 0))

        elif calculation_method == CalculationMethod.KARACHI:
            return self.from_angles_and_calculation_method(
                18.0, 18.0, calculation_method
            ).with_method_adjustments(PrayerAdjustments(0, 0, 1, 0, 0, 0))

        elif calculation_method == CalculationMethod.UMM_AL_QURA:
            return self.from_fajr_angle_isha_interval_and_calculation_method(
                18.5, 90, calculation_method
            )

        elif calculation_method == CalculationMethod.DUBAI:
            return self.from_angles_and_calculation_method(
                18.2, 18.2, calculation_method
            ).with_method_adjustments(PrayerAdjustments(0, -3, 3, 3, 3, 0))

        elif calculation_method == CalculationMethod.MOON_SIGHTING_COMMITTEE:
            return self.from_angles_and_calculation_method(
                18.0, 18.0, calculation_method
            ).with_method_adjustments(PrayerAdjustments(0, 0, 5, 0, 3, 0))

        elif calculation_method == CalculationMethod.NORTH_AMERICA:
            return self.from_angles_and_calculation_method(
                15.0, 15.0, calculation_method
            ).with_method_adjustments(PrayerAdjustments(0, 0, 1, 0, 0, 0))

        elif calculation_method == CalculationMethod.KUWAIT:
            return self.from_angles_and_calculation_method(
                18.0, 17.5, calculation_method
            )

        elif calculation_method == CalculationMethod.QATAR:
            return self.from_fajr_angle_isha_interval_and_calculation_method(
                18.0, 90, calculation_method
            )

        elif calculation_method == CalculationMethod.SINGAPORE:
            return self.from_angles_and_calculation_method(
                20.0, 18.0, calculation_method
            ).with_method_adjustments(PrayerAdjustments(0, 0, 1, 0, 0, 0))

        elif calculation_method == CalculationMethod.UOIF:
            return self.from_angles_and_calculation_method(
                12.0, 12.0, calculation_method
            )

        elif calculation_method == CalculationMethod.OTHER:
            return self.from_angles_and_calculation_method(0.0, 0.0, calculation_method)

        else:
            raise ValueError("Invalid CalculationMethod")
