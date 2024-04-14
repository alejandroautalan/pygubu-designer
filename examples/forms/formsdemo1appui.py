#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demo1.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class FormsDemo1AppUI:
    def __init__(self, master=None, on_first_object_cb=None):
        self.builder = pygubu.Builder(on_first_object=on_first_object_cb)
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Toplevel = self.builder.get_object(
            "toplevel1", master
        )
        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def on_submit_clicked(self):
        pass


if __name__ == "__main__":
    app = FormsDemo1AppUI()
    app.run()
