#!/usr/bin/python3
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
from counterappui import CounterAppUI

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "counter.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class CounterApp(CounterAppUI):
    def __init__(self, master=None):
        super().__init__(
            master,
            project_ui=PROJECT_UI,
            resource_paths=RESOURCE_PATHS,
            translator=None,
            on_first_object_cb=None,
        )
        self.builder.connect_callbacks(self)

    def on_count_clicked(self):
        value = self.counter_var.get()
        value += 1
        self.counter_var.set(value)


if __name__ == "__main__":
    app = CounterApp()
    app.run()
