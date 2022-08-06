from datetime import datetime, timedelta, timezone
import calendar
from typing import Tuple
from adhanpy.calculation.CalculationMethod import CalculationMethod
from adhanpy.calculation.CalculationParameters import CalculationParameters
from adhanpy.data.Prayer import Prayer
from adhanpy.astronomy.SolarTime import SolarTime
from adhanpy.data.Coordinates import Coordinates
from adhanpy.util.TimeComponents import TimeComponents
from adhanpy.util.DateComponents import DateComponents
from adhanpy.util.CalendarUtil import rounded_minute


def days_since_solstice(day_of_year: int, year: int, latitude: float) -> int:
    northern_offset = 10
    is_leap_year = calendar.isleap(year)

    southern_offset = 173 if is_leap_year else 172
    days_in_year = 366 if is_leap_year else 365

    if latitude >= 0:
        days_since_solstice = day_of_year + northern_offset
        if days_since_solstice >= days_in_year:
            days_since_solstice = days_since_solstice - days_in_year
    else:
        days_since_solstice = day_of_year - southern_offset
        if days_since_solstice < 0:
            days_since_solstice = days_since_solstice + days_in_year

    return days_since_solstice


def season_adjusted_morning_twilight(
    latitude: float, day: int, year: int, sunrise: datetime
):
    a = 75 + ((28.65 / 55.0) * abs(latitude))
    b = 75 + ((19.44 / 55.0) * abs(latitude))
    c = 75 + ((32.74 / 55.0) * abs(latitude))
    d = 75 + ((48.10 / 55.0) * abs(latitude))

    # final double adjustment;
    dyy = days_since_solstice(day, year, latitude)

    if dyy < 91:
        adjustment = a + (b - a) / 91.0 * dyy
    elif dyy < 137:
        adjustment = b + (c - b) / 46.0 * (dyy - 91)
    elif dyy < 183:
        adjustment = c + (d - c) / 46.0 * (dyy - 137)
    elif dyy < 229:
        adjustment = d + (c - d) / 46.0 * (dyy - 183)
    elif dyy < 275:
        adjustment = c + (b - c) / 46.0 * (dyy - 229)
    else:
        adjustment = b + (a - b) / 91.0 * (dyy - 275)

    return sunrise + timedelta(seconds=-int(round(adjustment * 60.0)))


def season_adjusted_evening_twilight(
    latitude: float, day: int, year: int, sunset: datetime
) -> datetime:
    a = 75 + ((25.60 / 55.0) * abs(latitude))
    b = 75 + ((2.050 / 55.0) * abs(latitude))
    c = 75 - ((9.210 / 55.0) * abs(latitude))
    d = 75 + ((6.140 / 55.0) * abs(latitude))

    dyy = days_since_solstice(day, year, latitude)
    if dyy < 91:
        adjustment = a + (b - a) / 91.0 * dyy
    elif dyy < 137:
        adjustment = b + (c - b) / 46.0 * (dyy - 91)
    elif dyy < 183:
        adjustment = c + (d - c) / 46.0 * (dyy - 137)
    elif dyy < 229:
        adjustment = d + (c - d) / 46.0 * (dyy - 183)
    elif dyy < 275:
        adjustment = c + (b - c) / 46.0 * (dyy - 229)
    else:
        adjustment = b + (a - b) / 91.0 * (dyy - 275)

    return sunset + timedelta(seconds=int(round(adjustment * 60.0)))


class PrayerTimes:
    def __init__(
        self,
        coordinates: Tuple[float, float],
        date: datetime,
        calculation_method: CalculationMethod = None,
        calculation_parameters: CalculationParameters = None,
    ):
        """
        Arguments:
            coordinates: (latitude, longitude)
            date: DateComponents
            calculation_parameters: CalculationParameters
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

        error = False
        if (
            transit is None
            or sunrise_components is None
            or sunset_components is None
            or tomorrow_sunrise_components is None
        ):
            error = True

        if error is False:
            temp_dhuhr = transit
            temp_sunrise = sunrise_components
            temp_maghrib = sunset_components

            time_components = TimeComponents.from_float(
                solar_time.afternoon(calculation_parameters.madhab.get_shadow_length())
            )

            if time_components is not None:
                temp_asr = time_components.date_components(date_components)

            # get night length
            tomorrow_sunrise = tomorrow_sunrise_components.date_components(
                tomorrow_date_components
            )

            night = (
                tomorrow_sunrise.timestamp() * 1000
                - sunset_components.timestamp() * 1000
            )

            time_components = TimeComponents.from_float(
                solar_time.hour_angle(-calculation_parameters.fajr_angle, False)
            )

            if time_components is not None:
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
                    seconds=-1 * int(night_fraction)
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
                    night_fraction = night / 7000
                    temp_isha = sunset_components + timedelta(
                        seconds=int(night_fraction)
                    )

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
            self.fajr = rounded_minute(
                (temp_fajr + timedelta(minutes=calculation_parameters.adjustments.fajr))
                + timedelta(minutes=calculation_parameters.method_adjustments.fajr)
            )

            self.sunrise = rounded_minute(
                (
                    temp_sunrise
                    + timedelta(minutes=calculation_parameters.adjustments.sunrise)
                )
                + timedelta(minutes=calculation_parameters.method_adjustments.sunrise)
            )

            self.dhuhr = rounded_minute(
                (
                    temp_dhuhr
                    + timedelta(minutes=calculation_parameters.adjustments.dhuhr)
                )
                + timedelta(minutes=calculation_parameters.method_adjustments.dhuhr)
            )

            self.asr = rounded_minute(
                (temp_asr + timedelta(minutes=calculation_parameters.adjustments.asr))
                + timedelta(minutes=calculation_parameters.method_adjustments.asr)
            )

            self.maghrib = rounded_minute(
                (
                    temp_maghrib
                    + timedelta(minutes=calculation_parameters.adjustments.maghrib)
                )
                + timedelta(minutes=calculation_parameters.method_adjustments.maghrib)
            )

            self.isha = rounded_minute(
                (temp_isha + timedelta(minutes=calculation_parameters.adjustments.isha))
                + timedelta(minutes=calculation_parameters.method_adjustments.isha)
            )

    def time_for_prayer(self, prayer: Prayer):
        if prayer == Prayer.FAJR:
            return self.fajr
        elif prayer == Prayer.SUNRISE:
            return self.sunrise
        elif prayer == Prayer.DHUHR:
            return self.dhuhr
        elif prayer == Prayer.ASR:
            return self.asr
        elif prayer == Prayer.MAGHRIB:
            return self.maghrib
        elif prayer == Prayer.ISHA:
            return self.isha
        else:
            return None
