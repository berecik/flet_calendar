from datetime import timedelta

import flet as ft
from utils import week_range, AnyDate


def day_tab(_date: AnyDate, content: ft.Control = None) -> ft.Tab:
    ft.Column(
        controls=[
            ft.Text(
                _date.strftime("%a"),
                text_align=ft.TextAlign.CENTER,
                no_wrap=True,
            ),
            ft.Text(
                _date.strftime("%d"),
                text_align=ft.TextAlign.CENTER,
                no_wrap=True,
            ),
        ],
        horizontal_alignment=ft.alignment.center
    )

    return ft.Tab(
        # tab_content=tab_content,
        content=content,
        text=_date.strftime("%a\n%d"),
    )


class CalendarTabs(ft.UserControl):
    def __init__(self, initial_date, get_content=None):
        super().__init__()
        self.date_label = ft.Text(
            # width=340,
            text_align=ft.TextAlign.CENTER
        )
        self.week_row = ft.Container()
        self.date = initial_date
        self.get_content = get_content or (lambda _date: ft.Text(str(_date)))
        self.days = None

    def set_days(self):
        week_tabs = []
        last_day = None
        index = self.date.weekday()

        for day in week_range(self.date):
            week_tabs.append(day_tab(day, self.get_content(day)))
            last_day = day

        self.date_label.value = last_day.strftime("%B %Y")
        self.week_row.content = ft.Tabs(
            selected_index=index,
            tabs=week_tabs,
            animation_duration=300,
            expand=1
        )

    def next_week(self, e):
        self.date += timedelta(days=7)
        self.set_days()
        self.update()

    def prev_week(self, e):
        self.date -= timedelta(days=7)
        self.set_days()
        self.update()

    def build(self):
        self.set_days()

        prev_button = ft.IconButton(
            icon=ft.icons.CHEVRON_LEFT,
            # width=60,
            on_click=self.prev_week
        )
        next_button = ft.IconButton(
            icon=ft.icons.CHEVRON_RIGHT,
            # width=60,
            on_click=self.next_week
        )
        ft.Row(
            [prev_button, self.date_label, next_button],
            # expand=1
        )

        return self.week_row
