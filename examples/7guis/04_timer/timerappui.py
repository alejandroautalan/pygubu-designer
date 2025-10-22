#!/usr/bin/python3
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu


class TimerAppUI:
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
        self.mainwindow: tk.Toplevel = self.builder.get_object(
            "mainwindow", master
        )

        self.gauge_var: tk.DoubleVar = None
        self.elapsed_time_var: tk.StringVar = None
        self.duration_var: tk.StringVar = None
        self.slider_var: tk.DoubleVar = None
        self.builder.import_variables(self)

    def run(self):
        self.mainwindow.mainloop()

    def on_slider_change(self, scale_value):
        pass

    def on_reset_clicked(self):
        pass
