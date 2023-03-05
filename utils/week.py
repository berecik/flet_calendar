from datetime import datetime, date, time, timedelta
from .date_time import AnyDate


def week_range(date_: AnyDate, week_start=0):
    weekday = date_.weekday()
    start_day_shift = (weekday + week_start) % 7
    _day = date_ - timedelta(days=start_day_shift)
    end_day = _day + timedelta(days=7)
    while _day < end_day:
        yield _day
        _day += timedelta(days=1)
