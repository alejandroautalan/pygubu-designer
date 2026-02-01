#!/usr/bin/python3
"""
Calculator UI

Calculator ui using pygubu bootstrap theme.

It's just the UI for example purpose.

UI source file: calculator.ui
"""
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
from demoappui import CalculatorAppUI

# Import style from pygubu bootstrap module
from pygubu.theming.bootstrap.style import Style


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "calculator.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class CalculatorApp(CalculatorAppUI):
    def __init__(self, master=None):
        super().__init__(
            master,
            project_ui=PROJECT_UI,
            resource_paths=RESOURCE_PATHS,
            translator=None,
            on_first_object_cb=None,
        )
        self.builder.connect_callbacks(self)

        # Setup application Theme
        self.style = Style(self.mainwindow)
        self.style.theme_use("pbs_darkly")


if __name__ == "__main__":
    app = CalculatorApp()
    app.run()
