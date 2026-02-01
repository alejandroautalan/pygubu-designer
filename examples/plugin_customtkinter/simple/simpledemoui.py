#!/usr/bin/python3
"""
Simple demo

Customtkinter simple demo.

UI source file: simple_demo.ui
"""
import pathlib
import tkinter as tk
import customtkinter
import pygubu


class SimpleDemoAppUI:
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

        self.radiobutton_var: tk.StringVar = None
        self.builder.import_variables(self)

    def run(self):
        self.mainwindow.mainloop()

    def button_callback(self):
        pass

    def slider_callback(self, value):
        pass
