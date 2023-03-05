import flet as ft
from controls import Calendar
from datetime import datetime


def main(page: ft.Page):
    text = ft.Text("Calendar page")
    page.add(text)
    page.add(Calendar(datetime.now()))


ft.app(main)
