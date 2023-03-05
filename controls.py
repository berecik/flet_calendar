import flet as ft
from datetime import date, datetime, timedelta
from utils import week_range, date_str, AnyDate


def day_button(_date: AnyDate):
    return ft.ElevatedButton(
        _date.strftime("%d"),
        width=60,
    )


def day_cell(_date: AnyDate):
    return ft.Column(
        controls=[
            ft.Text(
                _date.strftime("%a"),
                text_align=ft.TextAlign.CENTER,
                width=60,
                no_wrap=True,
                # text_align="center",
                color=ft.colors.ON_SURFACE_VARIANT,
            ),
            day_button(_date)
        ],
        alignment=ft.alignment.center
    )


class Calendar(ft.UserControl):
    def __init__(self, initial_date, get_container=None):
        super().__init__()
        self.date_label = ft.Text(
            width=340,
            text_align=ft.TextAlign.CENTER
        )
        self.week_row = ft.Row()
        self.date = initial_date
        self.get_container = get_container or (lambda controls: ft.Column(controls))

    def set_days(self):
        week_days = []
        last_day = None

        for day in week_range(self.date):
            week_days.append(day_cell(day))
            last_day = day

        self.date_label.value = last_day.strftime("%B %Y")
        self.week_row.controls = week_days

    def build(self):

        self.set_days()

        def next_week(e):
            self.date += timedelta(days=7)
            self.set_days()
            self.update()

        def prev_week(e):
            self.date -= timedelta(days=7)
            self.set_days()
            self.update()

        prev_button = ft.IconButton(
            icon=ft.icons.CHEVRON_LEFT,
            width=60,
            on_click=prev_week
        )
        next_button = ft.IconButton(
            icon=ft.icons.CHEVRON_RIGHT,
            width=60,
            on_click=next_week
        )
        control_row = ft.Row(
            [prev_button, self.date_label, next_button],
            # expand=1
        )

        container = ft.Container(
            ft.Column(
                [
                    control_row,
                    self.week_row
                ]
            ),
            width=460
        )

        return container
