#!/usr/bin/python3
"""
Simple demo

Customtkinter simple demo.

UI source file: simple_demo.ui
"""
import pathlib
import tkinter as tk
import pygubu
from simpledemoui import SimpleDemoAppUI

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "simple_demo.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class SimpleDemoApp(SimpleDemoAppUI):
    def __init__(self, master=None):
        super().__init__(
            master,
            project_ui=PROJECT_UI,
            resource_paths=RESOURCE_PATHS,
            translator=None,
            on_first_object_cb=None,
        )
        self.builder.connect_callbacks(self)

        self.progressbar_1 = self.builder.get_object("progressbar_1")
        self.slider_1 = self.builder.get_object("slider_1")
        self.optionmenu_1 = self.builder.get_object("optionmenu_1")
        self.combobox_1 = self.builder.get_object("combobox_1")

        # Init values
        self.slider_1.set(0.5)
        self.optionmenu_1.set("CTkOptionMenu")
        self.combobox_1.set("CTkComboBox")
        self.radiobutton_var.set(1)

    def button_callback(self):
        print("Button click", self.combobox_1.get())

    def slider_callback(self, value):
        self.progressbar_1.set(value)


if __name__ == "__main__":
    app = SimpleDemoApp()
    app.run()
