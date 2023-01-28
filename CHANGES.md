# Changelog

## v1.0.5
* Fix [#16](https://github.com/alphahm/adhanpy/issues/16) where method is either not provided or
explicitly set to `None` when initialising `CalculationParameters` results in an `AttributeError`
in `PrayerTimes`

## v1.0.4
* Fix [#4](https://github.com/alphahm/adhanpy/issues/4) where rounding of minutes function tried to
incorrectly set 60 for minutes on a datetime object.
* Bring support for Python 3.9
