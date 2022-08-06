from dataclasses import dataclass


@dataclass
class DateComponents:
    year: int
    month: int
    day: int

    @classmethod
    def from_utc(cls, date):
        return cls(date.year, date.month, date.day)
