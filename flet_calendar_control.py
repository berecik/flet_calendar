from datetime import date
from datetime import timedelta
from typing import Callable
from typing import Optional
from typing import Union

import flet as ft

from utils import AnyDate
from utils import week_range
from utils import day
from utils import equal_day


# from .day_cell import day_row_cell


def _print_date(_date: AnyDate):
    def __wrap_click(e):
        print(_date)

    return __wrap_click


class CalendarControl(ft.UserControl):
    def __init__(self,
                 initial_date,
                 cell_width: int = 60,
                 on_select: Optional[
                     Callable[
                         [AnyDate],
                         Optional[
                             Callable[
                                 [object],
                                 Optional[
                                     Union[
                                         bool,
                                         Callable[
                                             [],
                                             None
                                         ]
                                     ]
                                 ]
                             ]
                         ]
                     ]
                 ] = None,
                 check_date: Optional[
                     Callable[
                         [AnyDate],
                         bool
                     ]
                 ] = None,
                 min_date: Optional[AnyDate] = None,
                 max_date: Optional[AnyDate] = None,
                 weekdays=None
                 ):
        super().__init__()
        if weekdays is None:
            weekdays = range(5)  # as default is range Mon-Fri
        self.weekdays = set(weekdays)
        self.max_date = max_date or date.today() + timedelta(days=15)
        self.min_date = min_date or date.today() - timedelta(days=15)
        self.on_select = on_select or _print_date
        self.cell_width = cell_width
        self.date_label = ft.Text(
            text_align=ft.TextAlign.CENTER
        )
        self.week_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        self.date = initial_date
        self.get_date = check_date or (lambda _date: True)

    def in_range(self, _date: AnyDate):
        if self.max_date and \
                day(_date) + timedelta(days=7-_date.weekday()) > day(self.max_date):
            return False
        if self.min_date and \
                day(_date) - timedelta(days=_date.weekday()) < day(self.min_date):
            return False
        return True

    def check_day(self, _date: AnyDate):
        return _date.weekday() in self.weekdays

    def equal_day(self, _date: AnyDate):
        return equal_day(self.date, _date)
    
    
    def get_button(self):
        return ft.ElevatedButton()

    def day_button(self, _date: AnyDate):
        button = self.get_button()
        button.text = _date.strftime("%d")

        if self.equal_day(_date):
            button.bgcolor = ft.colors.SECONDARY
            button.color = ft.colors.BACKGROUND
            button.disabled = True
            return button

        on_select = self.on_select(_date)
        
        if on_select:
            def __click_wrapper(e):
                posteriori = on_select(e)
                if posteriori is not False:
                    self.date = _date
                    self.set_days()
                    self.update()
                if callable(posteriori):
                    posteriori()
            button.on_click = __click_wrapper
        else:
            button.disabled = True

        return button

    def day_row_cell(self, _date: AnyDate, cell_width):
        return ft.Column(
            controls=[
                ft.Text(
                    _date.strftime("%a"),
                    text_align=ft.TextAlign.CENTER,
                    no_wrap=True,
                    color=ft.colors.ON_SURFACE_VARIANT,
                    width=cell_width,
                    # expand=True
                ),
                self.day_button(_date)
            ],
            horizontal_alignment=ft.alignment.center,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )

    def set_days(self):
        week_days = []
        last_day = None

        for day in week_range(self.date):
            if self.check_day(day):
                week_days.append(self.day_row_cell(day, self.cell_width))
                last_day = day

        self.date_label.value = last_day.strftime("%B %Y")
        self.week_row.controls = week_days

    def build(self):
        self.set_days()

        next_button = ft.IconButton(
            icon=ft.icons.CHEVRON_RIGHT,
            disabled=True
        )
        next_date = self.date + timedelta(days=7)
        if self.in_range(next_date):
            def next_week(e):
                self.date += timedelta(days=7)
                self.set_days()
                self.update()

            next_button.on_click = next_week
            next_button.disabled = False

        prev_button = ft.IconButton(
            icon=ft.icons.CHEVRON_LEFT,
            disabled=True
        )
        prev_date = self.date - timedelta(days=7)
        if self.in_range(prev_date):
            def prev_week(e):
                self.date -= timedelta(days=7)
                self.set_days()
                self.update()

            prev_button.on_click = prev_week
            prev_button.disabled = False

        control_row = ft.Row(
            [prev_button, self.date_label, next_button],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        container = ft.Container(
            ft.Column(
                [
                    control_row,
                    self.week_row
                ],
                horizontal_alignment=ft.alignment.center
            ),
        )

        return container
