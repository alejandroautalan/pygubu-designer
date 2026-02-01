#!/usr/bin/python3
"""
Radiobutton Example

Awesome tkinter radiobutton example.

UI source file: radioapp.ui
"""
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
from radiobuttonui import RadiobuttonAppUI

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "radioapp.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class RadiobuttonApp(RadiobuttonAppUI):
    def __init__(self, master=None):
        super().__init__(
            master,
            project_ui=PROJECT_UI,
            resource_paths=RESOURCE_PATHS,
            translator=None,
            on_first_object_cb=None,
        )
        self.builder.connect_callbacks(self)


if __name__ == "__main__":
    app = RadiobuttonApp()
    app.run()
