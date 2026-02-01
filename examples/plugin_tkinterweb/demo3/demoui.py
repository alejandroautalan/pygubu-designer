#!/usr/bin/python3
"""
Tkinterweb Notebook demo

A simple demo for Notebook widget.

UI source file: demo_notebook.ui
"""
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu


class DemoAppUI:
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
        self.mainwindow: tk.Tk = self.builder.get_object("tk1", master)

    def run(self):
        self.mainwindow.mainloop()
