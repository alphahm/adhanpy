import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from adhanpy.util.DateComponents import DateComponents


@dataclass
class TimeComponents:
    hours: int
    minutes: int
    seconds: int

    @classmethod
    def from_float(cls, value):
        if math.isinf(value) or math.isnan(value):
            return None

        hours = math.floor(value)
        minutes = math.floor((value - hours) * 60.0)
        seconds = math.floor((value - (hours + minutes / 60.0)) * 60 * 60)
        return cls(int(hours), int(minutes), int(seconds))

    def date_components(self, date_components: DateComponents) -> datetime:
        date_time = datetime(
            date_components.year,
            date_components.month,
            date_components.day,
            0,
            self.minutes,
            self.seconds,
            tzinfo=timezone.utc,
        )
        date_time = date_time + timedelta(hours=self.hours)

        return date_time
