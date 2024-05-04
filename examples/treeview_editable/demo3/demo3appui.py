#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demo3.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class DemoAppUI:
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Toplevel = self.builder.get_object(
            "toplevel1", master
        )

        self.allow_edit: tk.BooleanVar = None
        self.builder.import_variables(self)

        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def on_cell_edited(self, event=None):
        pass

    def on_editors_unfocused(self, event=None):
        pass

    def on_inplace_edit(self, event=None):
        pass

    def on_row_selected(self, event=None):
        pass


if __name__ == "__main__":
    app = DemoAppUI()
    app.run()
