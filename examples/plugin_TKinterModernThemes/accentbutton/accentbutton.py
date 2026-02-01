#!/usr/bin/python3
"""
TKMT AccentButton

AccentButton example.

UI source file: accentbutton.ui
"""
import pathlib
import tkinter as tk
import pygubu
from accentbuttonui import AppUI

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "accentbutton.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class App(AppUI):
    def __init__(self, master=None):
        super().__init__(
            master,
            project_ui=PROJECT_UI,
            resource_paths=RESOURCE_PATHS,
            translator=None,
            on_first_object_cb=None,
        )
        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.run()

    def handle_btn_click(self):
        print("Button Clicked!")


if __name__ == "__main__":
    app = App()
    app.run()
