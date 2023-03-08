import flet as ft

from utils import AnyDate


def day_button(_date: AnyDate):
    return ft.ElevatedButton(
        _date.strftime("%d"),
        # width=60,
    )


def day_row_cell(_date: AnyDate, cell_width):
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
            day_button(_date)
        ],
        horizontal_alignment=ft.alignment.center,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )