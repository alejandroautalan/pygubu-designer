#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "accentbutton.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class AppUI:
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = self.builder.get_object("themedtkinterframe1", master)
        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def handle_btn_click(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = AppUI(root)
    app.run()
