#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "messagebox.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class CustomMessageBoxUI:
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: pygubu.builder.widgets.dialog = (
            self.builder.get_object("dialog1", master)
        )
        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def btn_ok_clicked(self):
        pass

    def on_dialog_close(self, event=None):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomMessageBoxUI(root)
    app.run()
