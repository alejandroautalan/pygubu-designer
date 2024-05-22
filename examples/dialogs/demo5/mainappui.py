#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "mainapp.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class MyDemoAppUI:
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Tk = self.builder.get_object("tk1", master)

        self.fullscreen_var: tk.BooleanVar = None
        self.dialog_fullscreen_var: tk.BooleanVar = None
        self.builder.import_variables(self)

        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def on_fullscreen_clicked(self):
        pass

    def on_showmodal_clicked(self):
        pass


if __name__ == "__main__":
    app = MyDemoAppUI()
    app.run()
