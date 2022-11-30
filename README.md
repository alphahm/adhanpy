# adhanpy

[![License: MIT](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)
![pytest](https://github.com/alphahm/adhanpy/actions/workflows/test.yml/badge.svg)

This is a port of [batoulapps/adhan-java](https://github.com/batoulapps/adhan-java), a prayer times program, from Java to Python.
As it stands the project reuses most of the structure of the original project but may differ through refactoring and in an effort
to rewrite in a more pythonic way where it makes sense.
Like the original project there are no external dependencies except in development where [pytest](https://github.com/pytest-dev/pytest)
and other development tools are made use of.

## Requirements

* Python >= 3.9

## Installation

```
pip install adhanpy
```

## Usage

Create a `PrayerTimes` object by passing geo coodinates, datetime and either passing a calculation method:

```python
prayer_times = PrayerTimes(coordinates, today, CalculationMethod.MOON_SIGHTING_COMMITTEE)
```

or a calculation parameters object allowing to choose from different parameters such as angles:

```python
parameters = CalculationParameters(fajr_angle=18, isha_angle=18)
prayer_times = PrayerTimes(coordinates, today, calculation_parameters=parameters)
```

If passing a calculation method to the calculation parameters object, the calculation method
will have precedence and will overwrite other parameters you may have also passed.

For instance the MOON_SIGHTING_COMMITTEE method uses a fajr angle of 18 and if for
instance the calculation parameters object is created by passing a different fajr angle the
latter will be ignored:

```python
parameters = CalculationParameters(fajr_angle=12, method=CalculationMethod.MOON_SIGHTING_COMMITTEE)
prayer_times = PrayerTimes(coordinates, today, calculation_parameters=parameters)
print(parameters.fajr_angle)
# 18.0 (the fajr_angle argument has been ignored)
```

Times are returned in UTC time via datetime objects, for convenience it is possible to directly pass
a ZoneInfo object to PrayerTimes:

```python
london_zone = ZoneInfo("Europe/London")
prayer_times = PrayerTimes(
    coordinates,
    today,
    CalculationMethod.MOON_SIGHTING_COMMITTEE,
    time_zone=london_zone,
)

# this will display the time in the chosen time zone
print(f"Fajr: {prayer_times.fajr.strftime('%H:%M')}")
```

or convert to a different timezone later, each prayer time object is in fact a datetime object:

```python
prayer_times = PrayerTimes(
    coordinates,
    today,
    CalculationMethod.MOON_SIGHTING_COMMITTEE,
)

# the following will be in UTC
print(f"Fajr: {prayer_times.fajr.strftime('%H:%M')}")

# and to use a different timezone on the datetime object itself:
london_zone = ZoneInfo("Europe/London")
print(f"Fajr: {prayer_times.fajr.astimezone(london_zone).strftime('%H:%M')}")
```

A full example is located in `src/example` of the project directory.

## Development

To install adhanpy for development purposes, run the following:

```
python3 -m virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## Licence

MIT

## Acknowledgments

Credits go to the author of the original implementation in Java and other languages, especially the very complex astronomy
formulas.
