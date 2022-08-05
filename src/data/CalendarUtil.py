from datetime import datetime


def rounded_minute(when: datetime) -> datetime:
    """
    Date and time with a rounded minute
    This returns a date with the seconds rounded and added to the minute
    when the date and time eturn the date and time with 0 seconds and
    minutes including rounded seconds
    """
    minute = when.minute
    second = when.second
    rounded = when.replace(minute=int(minute + round(second / 60)), second=0)
    return rounded
