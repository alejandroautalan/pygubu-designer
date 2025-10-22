#!/usr/bin/python3
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
from tempconvappui import TempconvAppUI

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "tempconv.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class TempconvApp(TempconvAppUI):
    def __init__(self, master=None):
        super().__init__(
            master,
            project_ui=PROJECT_UI,
            resource_paths=RESOURCE_PATHS,
            translator=None,
            on_first_object_cb=None,
        )
        self.builder.connect_callbacks(self)

        self.tempc = self.builder.get_object("tempc")
        self.tempf = self.builder.get_object("tempf")

    def temp_validate(self, d_action, p_entry_value, w_entry_name):
        is_valid = True
        if d_action == "1":  # Insert
            try:
                temperature = float(p_entry_value)
                widget = self.mainwindow.nametowidget(w_entry_name)
                if widget is self.tempc:
                    self.calculate_fahrenheit(temperature)
                else:
                    self.calculate_celsius(temperature)
            except ValueError:
                is_valid = False
        return is_valid

    def calculate_celsius(self, f):
        celsius = (f - 32) * (5 / 9)
        celsius = f"{celsius:.2f}"
        self.tempc_var.set(celsius)

    def calculate_fahrenheit(self, c):
        fahrenheit = c * (9 / 5) + 32
        fahrenheit = f"{fahrenheit:.2f}"
        self.tempf_var.set(fahrenheit)


if __name__ == "__main__":
    app = TempconvApp()
    app.run()
