#!/usr/bin/python3
"""
awesometkinter demo

Same as demo.py from awesometkinter examples.

UI source file: demo.ui
"""
import pathlib
import tkinter as tk
import pygubu
from demoappui import DemoAppUI

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demo.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class DemoApp(DemoAppUI):
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
    app = DemoApp()
    app.run()
