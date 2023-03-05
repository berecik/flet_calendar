from datetime import datetime, date, time
from typing import Union, TypeAlias

AnyDate: TypeAlias = Union[datetime, date]


def date_str(_date: AnyDate):
    return _date.strftime("%a, %d %b, %Y")


def time_str(_time: AnyDate):
    return _time.strftime("%H:%M")

