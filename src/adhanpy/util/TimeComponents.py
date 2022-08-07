from __future__ import annotations
import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional
from adhanpy.util.DateComponents import DateComponents


@dataclass
class TimeComponents:
    hours: int
    minutes: int
    seconds: int

    @classmethod
    def from_float(cls, value: float) -> Optional[TimeComponents]:
        if math.isinf(value) or math.isnan(value):
            return None

        minutes, seconds = divmod(value * 60 * 60, 60)
        hours, minutes = divmod(minutes, 60)
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
