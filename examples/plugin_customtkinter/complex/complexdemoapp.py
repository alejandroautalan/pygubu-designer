#!/usr/bin/python3
"""
Complex demo

Customtkinter complex demo.

UI source file: complex_demo.ui
"""
import pathlib
import tkinter as tk
import pygubu
import customtkinter
from complexdemoappui import ComplexDemoAppUI

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "complex_demo.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class ComplexDemoApp(ComplexDemoAppUI):
    def __init__(self, master=None):
        super().__init__(
            master,
            project_ui=PROJECT_UI,
            resource_paths=RESOURCE_PATHS,
            translator=None,
            on_first_object_cb=None,
        )
        self.builder.connect_callbacks(self)

        #
        # Initial state configuration
        #
        self.progressbar_1 = self.builder.get_object("progressbar_1")
        self.slider_1 = self.builder.get_object("slider_1")
        self.slider_2 = self.builder.get_object("slider_2")
        self.progressbar_2 = self.builder.get_object("progressbar_2")
        self.progressbar_3 = self.builder.get_object("progressbar_3")
        self.checkbox_1 = self.builder.get_object("checkbox_1")
        self.switch_1 = self.builder.get_object("switch_1")

        self.progressbar_1.start()

        self.slider_1.configure(command=self.progressbar_2.set)
        self.slider_2.configure(command=self.progressbar_3.set)

        self.checkbox_1.select()
        self.switch_1.select()

        self.radio_var.set(0)
        self.appearance_var.set("System")
        self.scaling_var.set("100%")

    def sidebar_button_event(self):
        print("sidebar_button click")

    def change_appearance_mode_event(self, current_value):
        customtkinter.set_appearance_mode(current_value)

    def change_scaling_event(self, current_value):
        new_scaling_float = int(current_value.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(
            text="Type in a number:", title="CTkInputDialog"
        )
        print("CTkInputDialog:", dialog.get_input())

    def on_switch_toggle(self):
        print("switch 1 toggle")

    def on_segbtn_clicked(self, current_value):
        print(current_value)


if __name__ == "__main__":
    app = ComplexDemoApp()
    app.run()
