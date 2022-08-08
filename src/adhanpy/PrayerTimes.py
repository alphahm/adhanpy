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
                "Only one of calculation_method or calculation_parameters must be passed."
            )

        self.calculation_parameters = calculation_parameters

        if self.calculation_parameters is None:
            self.calculation_parameters = CalculationParameters(
                method=calculation_method
            )

        latitude, longitude = coordinates
        self.coordinates = Coordinates(latitude, longitude)
        self._date_components = DateComponents.from_utc(date)
        self.time_zone = time_zone

        self._prayer_date = datetime(
            self._date_components.year,
            self._date_components.month,
            self._date_components.day,
            tzinfo=timezone.utc,
        )

        self._day_of_year = self._prayer_date.timetuple().tm_yday

        tomorrow_date = self._prayer_date + timedelta(days=1)
        tomorrow_date_components = DateComponents.from_utc(tomorrow_date)

        self._solar_time = SolarTime(self._date_components, self.coordinates)

        time_components = TimeComponents.from_float(self._solar_time.transit)
        transit = (
            None
            if time_components is None
            else time_components.date_components(self._date_components)
        )

        time_components = TimeComponents.from_float(self._solar_time.sunrise)
        self._sunrise_components = (
            None
            if time_components is None
            else time_components.date_components(self._date_components)
        )

        time_components = TimeComponents.from_float(self._solar_time.sunset)
        self._sunset_components = (
            None
            if time_components is None
            else time_components.date_components(self._date_components)
        )

        tomorrow_solar_time = SolarTime(tomorrow_date_components, self.coordinates)
        tomorrow_sunrise_components = TimeComponents.from_float(
            tomorrow_solar_time.sunrise
        )

        if (
            transit is None
            or self._sunrise_components is None
            or self._sunset_components is None
            or tomorrow_sunrise_components is None
        ):
            raise RuntimeError

        # get night length
        tomorrow_sunrise = tomorrow_sunrise_components.date_components(
            tomorrow_date_components
        )
        self.night_length = (
            tomorrow_sunrise.timestamp() * 1000
            - self._sunset_components.timestamp() * 1000
        )
        self.night_portions = self.calculation_parameters.night_portions()

        # Assign final times to properties with all offsets
        self._set_fajr()
        self._set_sunrise()
        self._set_dhuhr(transit)
        self._set_asr()
        self._set_maghrib()
        self._set_isha(self._sunset_components)

        self._adjust_prayers_time_zone()

    def _set_fajr(self):
        temp_fajr = None
        if time_components := TimeComponents.from_float(
            self._solar_time.hour_angle(-self.calculation_parameters.fajr_angle, False)
        ):
            temp_fajr = time_components.date_components(self._date_components)

        if (
            self.calculation_parameters.method
            == CalculationMethod.MOON_SIGHTING_COMMITTEE
        ):
            if self.coordinates.latitude >= 55:
                temp_fajr = self._sunrise_components + timedelta(
                    seconds=-1 * int(self.night_length / 7000)
                )

            safe_fajr = season_adjusted_morning_twilight(
                self.coordinates.latitude,
                self._day_of_year,
                self._prayer_date.year,
                self._sunrise_components,
            )
        else:
            portion = self.night_portions.fajr
            night_fraction = int(portion * self.night_length / 1000)
            safe_fajr = self._sunrise_components + timedelta(
                seconds=-1 * night_fraction
            )

        if temp_fajr is None or temp_fajr < safe_fajr:
            temp_fajr = safe_fajr

        self.fajr = self._rounded_minute(
            self.calculation_parameters.adjustments,
            self.calculation_parameters.method_adjustments,
            "fajr",
            temp_fajr,
        )

    def _set_sunrise(self):
        self.sunrise = self._rounded_minute(
            self.calculation_parameters.adjustments,
            self.calculation_parameters.method_adjustments,
            "sunrise",
            self._sunrise_components,
        )

    def _set_dhuhr(self, time):
        self.dhuhr = self._rounded_minute(
            self.calculation_parameters.adjustments,
            self.calculation_parameters.method_adjustments,
            "dhuhr",
            time,
        )

    def _set_asr(self):
        if time_components := TimeComponents.from_float(
            self._solar_time.afternoon(
                self.calculation_parameters.madhab.get_shadow_length()
            )
        ):
            if temp_asr := time_components.date_components(self._date_components):
                self.asr = self._rounded_minute(
                    self.calculation_parameters.adjustments,
                    self.calculation_parameters.method_adjustments,
                    "asr",
                    temp_asr,
                )
        try:
            self.asr.hour
        except:
            raise RuntimeError

    def _set_maghrib(self):
        self.maghrib = self._rounded_minute(
            self.calculation_parameters.adjustments,
            self.calculation_parameters.method_adjustments,
            "maghrib",
            self._sunset_components,
        )

    def _set_isha(self, sunset):
        # Isha calculation with check against safe value
        temp_isha = None
        try:
            if self.calculation_parameters.isha_interval < 1:
                raise ValueError("Isha interval is either not defined or less than 1.")

            temp_isha = sunset + timedelta(
                seconds=self.calculation_parameters.isha_interval * 60
            )
        except:
            timeComponents = TimeComponents.from_float(
                self._solar_time.hour_angle(
                    -self.calculation_parameters.isha_angle, True
                )
            )

            if timeComponents is not None:
                temp_isha = timeComponents.date_components(self._date_components)

            if (
                self.calculation_parameters.method
                == CalculationMethod.MOON_SIGHTING_COMMITTEE
                and self.coordinates.latitude >= 55
            ):
                night_fraction = int(self.night_length / 7000)
                temp_isha = self._sunset_components + timedelta(seconds=night_fraction)

            if (
                self.calculation_parameters.method
                == CalculationMethod.MOON_SIGHTING_COMMITTEE
            ):
                safe_isha = season_adjusted_evening_twilight(
                    self.coordinates.latitude,
                    self._day_of_year,
                    self._date_components.year,
                    self._sunset_components,
                )
            else:
                portion = self.night_portions.isha
                night_fraction = int(portion * self.night_length / 1000)

                safe_isha = self._sunset_components + timedelta(
                    seconds=int(night_fraction)
                )

            if temp_isha is None or temp_isha > safe_isha:
                temp_isha = safe_isha

        self.isha = self._rounded_minute(
            self.calculation_parameters.adjustments,
            self.calculation_parameters.method_adjustments,
            "isha",
            temp_isha,
        )

    def _rounded_minute(
        self, adjustments, method_adjustments, prayer_name, temp_prayer
    ):
        prayer_adjustments = getattr(adjustments, prayer_name)
        method_prayer_adjustments = getattr(method_adjustments, prayer_name)
        return rounded_minute(
            (temp_prayer + timedelta(minutes=prayer_adjustments))
            + timedelta(minutes=method_prayer_adjustments)
        )

    def _adjust_prayers_time_zone(self):
        if self.time_zone is not None:
            self.fajr = self.fajr.astimezone(self.time_zone)
            self.sunrise = self.sunrise.astimezone(self.time_zone)
            self.dhuhr = self.dhuhr.astimezone(self.time_zone)
            self.asr = self.asr.astimezone(self.time_zone)
            self.maghrib = self.maghrib.astimezone(self.time_zone)
            self.isha = self.isha.astimezone(self.time_zone)
