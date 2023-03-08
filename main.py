from datetime import datetime

import flet as ft
from flet_calendar_control import CalendarControl


def main(page: ft.Page):
    text = ft.Text("CalendarControl page")
    page.add(text)
    page.add(CalendarControl(datetime.now()))


ft.app(main)
