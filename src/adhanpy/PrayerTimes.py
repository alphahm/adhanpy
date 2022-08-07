from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from typing import Tuple
from adhanpy.calculation.CalculationMethod import CalculationMethod
from adhanpy.calculation.CalculationParameters import CalculationParameters
from adhanpy.calculation.Twilight import (
    season_adjusted_evening_twilight,
    season_adjusted_morning_twilight,
)
from adhanpy.data.Prayer import Prayer
from adhanpy.astronomy.SolarTime import SolarTime
from adhanpy.data.Coordinates import Coordinates
from adhanpy.util.TimeComponents import TimeComponents
from adhanpy.util.DateComponents import DateComponents
from adhanpy.util.CalendarUtil import rounded_minute


class PrayerTimes:
    def __init__(
        self,
        coordinates: Tuple[float, float],
        date: datetime,
        calculation_method: CalculationMethod = None,
        calculation_parameters: CalculationParameters = None,
        time_zone: ZoneInfo = None,
    ):
        """
        Arguments:
            coordinates: (latitude, longitude)
            date: DateComponents
            calculation_parameters: CalculationParameters
            time_zone: example ZoneInfo("Europe/London")
        Returns:
            PrayerTimes object with UTC datetimes for fajr, sunrise, dhuhr, asr, maghrib and isha
        """

        if (calculation_parameters and calculation_method) or not (
            calculation_parameters or calculation_method
        ):
            raise ValueError(
                "Either calculation_method (CalculationMethod) or calculation_parameters (CalculationParameters) can be passed."
            )

        if calculation_parameters is None:
            calculation_parameters = CalculationParameters(method=calculation_method)

        temp_fajr = None
        temp_sunrise = None
        temp_dhuhr = None
        temp_asr = None
        temp_maghrib = None
        temp_isha = None

        self.coordinates = Coordinates(coordinates[0], coordinates[1])
        date_components = DateComponents.from_utc(date)
        self.time_zone = time_zone

        prayer_date = datetime(
            date_components.year,
            date_components.month,
            date_components.day,
            tzinfo=timezone.utc,
        )

        day_of_year = prayer_date.timetuple().tm_yday

        tomorrow_date = prayer_date + timedelta(days=1)
        tomorrow_date_components = DateComponents.from_utc(tomorrow_date)

        solar_time = SolarTime(date_components, self.coordinates)

        time_components = TimeComponents.from_float(solar_time.transit)
        transit = (
            None
            if time_components is None
            else time_components.date_components(date_components)
        )

        time_components = TimeComponents.from_float(solar_time.sunrise)
        sunrise_components = (
            None
            if time_components is None
            else time_components.date_components(date_components)
        )

        time_components = TimeComponents.from_float(solar_time.sunset)
        sunset_components = (
            None
            if time_components is None
            else time_components.date_components(date_components)
        )

        tomorrow_solar_time = SolarTime(tomorrow_date_components, self.coordinates)
        tomorrow_sunrise_components = TimeComponents.from_float(
            tomorrow_solar_time.sunrise
        )

        error = (
            transit is None
            or sunrise_components is None
            or sunset_components is None
            or tomorrow_sunrise_components is None
        )

        if error is False:
            temp_dhuhr = transit
            temp_sunrise = sunrise_components
            temp_maghrib = sunset_components

            if time_components := TimeComponents.from_float(
                solar_time.afternoon(calculation_parameters.madhab.get_shadow_length())
            ):
                temp_asr = time_components.date_components(date_components)

            # get night length
            tomorrow_sunrise = tomorrow_sunrise_components.date_components(
                tomorrow_date_components
            )

            night = (
                tomorrow_sunrise.timestamp() * 1000
                - sunset_components.timestamp() * 1000
            )

            if time_components := TimeComponents.from_float(
                solar_time.hour_angle(-calculation_parameters.fajr_angle, False)
            ):
                temp_fajr = time_components.date_components(date_components)

            if (
                calculation_parameters.method
                == CalculationMethod.MOON_SIGHTING_COMMITTEE
                and self.coordinates.latitude >= 55
            ):
                temp_fajr = sunrise_components + timedelta(
                    seconds=-1 * int(night / 7000)
                )

            night_portions = calculation_parameters.night_portions()

            if (
                calculation_parameters.method
                == CalculationMethod.MOON_SIGHTING_COMMITTEE
            ):
                safe_fajr = season_adjusted_morning_twilight(
                    self.coordinates.latitude,
                    day_of_year,
                    prayer_date.year,
                    sunrise_components,
                )
            else:
                portion = night_portions.fajr
                night_fraction = int(portion * night / 1000)
                safe_fajr = sunrise_components + timedelta(
                    seconds=-1 * night_fraction
                )

            if temp_fajr is None or temp_fajr < safe_fajr:
                temp_fajr = safe_fajr

            # Isha calculation with check against safe value
            try:
                if calculation_parameters.isha_interval < 1:
                    raise ValueError(
                        "Isha interval is either not defined or less than 1."
                    )

                temp_isha = temp_maghrib + timedelta(
                    seconds=calculation_parameters.isha_interval * 60
                )
            except:
                timeComponents = TimeComponents.from_float(
                    solar_time.hour_angle(-calculation_parameters.isha_angle, True)
                )

                if timeComponents is not None:
                    temp_isha = timeComponents.date_components(date_components)

                if (
                    calculation_parameters.method
                    == CalculationMethod.MOON_SIGHTING_COMMITTEE
                    and self.coordinates.latitude >= 55
                ):
                    night_fraction = int(night / 7000)
                    temp_isha = sunset_components + timedelta(seconds=night_fraction)

                if (
                    calculation_parameters.method
                    == CalculationMethod.MOON_SIGHTING_COMMITTEE
                ):
                    safe_isha = season_adjusted_evening_twilight(
                        self.coordinates.latitude,
                        day_of_year,
                        date_components.year,
                        sunset_components,
                    )
                else:
                    portion = night_portions.isha
                    night_fraction = int(portion * night / 1000)

                    safe_isha = sunset_components + timedelta(
                        seconds=int(night_fraction)
                    )

                if temp_isha is None or temp_isha > safe_isha:
                    temp_isha = safe_isha

        if error is True or temp_asr is None:
            # if we don't have all prayer times then initialization failed
            self.fajr = None
            self.sunrise = None
            self.dhuhr = None
            self.asr = None
            self.maghrib = None
            self.isha = None
        else:
            # Assign final times to public struct members with all offsets
            self.fajr = self._rounded_minute(
                calculation_parameters.adjustments,
                calculation_parameters.method_adjustments,
                "fajr",
                temp_fajr,
            )
            self.sunrise = self._rounded_minute(
                calculation_parameters.adjustments,
                calculation_parameters.method_adjustments,
                "sunrise",
                temp_sunrise,
            )
            self.dhuhr = self._rounded_minute(
                calculation_parameters.adjustments,
                calculation_parameters.method_adjustments,
                "dhuhr",
                temp_dhuhr,
            )
            self.asr = self._rounded_minute(
                calculation_parameters.adjustments,
                calculation_parameters.method_adjustments,
                "asr",
                temp_asr,
            )
            self.maghrib = self._rounded_minute(
                calculation_parameters.adjustments,
                calculation_parameters.method_adjustments,
                "maghrib",
                temp_maghrib,
            )
            self.isha = self._rounded_minute(
                calculation_parameters.adjustments,
                calculation_parameters.method_adjustments,
                "isha",
                temp_isha,
            )

        if time_zone is not None:
            self._adjust_prayers_time_zone()

    def time_for_prayer(self, prayer: Prayer):
        match prayer:
            case Prayer.FAJR:
                return self.fajr
            case Prayer.SUNRISE:
                return self.sunrise
            case Prayer.DHUHR:
                return self.dhuhr
            case Prayer.ASR:
                return self.asr
            case Prayer.MAGHRIB:
                return self.maghrib
            case Prayer.ISHA:
                return self.isha
        return None

    def _rounded_minute(
        self, adjustments, method_adjustments, prayer_name, temp_prayer
    ):
        prayer_adjustments = getattr(adjustments, prayer_name)
        method_prayer_adjustments = getattr(method_adjustments, prayer_name)
        return rounded_minute(
            (temp_prayer + timedelta(minutes=prayer_adjustments)) + timedelta(minutes=method_prayer_adjustments)
        )

    def _adjust_prayers_time_zone(self):
        self.fajr = self.fajr.astimezone(self.time_zone)
        self.sunrise = self.sunrise.astimezone(self.time_zone)
        self.dhuhr = self.dhuhr.astimezone(self.time_zone)
        self.asr = self.asr.astimezone(self.time_zone)
        self.maghrib = self.maghrib.astimezone(self.time_zone)
        self.isha = self.isha.astimezone(self.time_zone)
