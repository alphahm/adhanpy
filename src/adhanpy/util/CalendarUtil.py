from datetime import datetime


def rounded_minute(when: datetime) -> datetime:
    """
    Round the seconds of a datetime object to 0 or 1 minute
    and add it to the datetime's minutes when possible or
    drop the seconds
    when: datetime object
    return: datetime object with seconds rounded to the nearest minute
    """
    minute = when.minute
    second = when.second

    try:
        rounded = when.replace(minute=int(minute + round(second / 60)), second=0)
    except ValueError:
        rounded = when.replace(second=0)

    return rounded
