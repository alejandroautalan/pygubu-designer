#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from demoappui import CalculatorAppUI

# Import style from pygubu bootstrap module
from pygubu.theming.bootstrap.style import Style


class CalculatorApp(CalculatorAppUI):
    def __init__(self, master=None):
        super().__init__(master)

        # Setup application Theme
        self.style = Style(self.mainwindow)
        self.style.theme_use("pbs_darkly")


if __name__ == "__main__":
    app = CalculatorApp()
    app.run()
