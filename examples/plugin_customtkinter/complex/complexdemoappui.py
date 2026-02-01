#!/usr/bin/python3
"""
Complex demo

Customtkinter complex demo.

UI source file: complex_demo.ui
"""
import pathlib
import tkinter as tk
import customtkinter
import pygubu


class ComplexDemoAppUI:
    def __init__(
        self,
        master=None,
        *,
        project_ui,
        resource_paths=None,
        translator=None,
        on_first_object_cb=None,
        data_pool=None,
    ):
        self.builder = pygubu.Builder(
            translator=translator,
            on_first_object=on_first_object_cb,
            data_pool=data_pool,
        )
        self.builder.add_from_file(project_ui)
        if resource_paths is not None:
            self.builder.add_resource_paths(resource_paths)
        # Main widget
        self.mainwindow: customtkinter.CTk = self.builder.get_object(
            "ctk1", master
        )

        self.appearance_var: tk.StringVar = None
        self.scaling_var: tk.StringVar = None
        self.radio_var: tk.StringVar = None
        self.builder.import_variables(self)

    def run(self):
        self.mainwindow.mainloop()

    def sidebar_button_event(self):
        pass

    def change_appearance_mode_event(self, current_value):
        pass

    def change_scaling_event(self, current_value):
        pass

    def open_input_dialog_event(self):
        pass

    def on_switch_toggle(self):
        pass

    def on_segbtn_clicked(self, current_value):
        pass
