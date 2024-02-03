#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "about_dialog.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class AboutDialogUI:
    def __init__(self, master=None, translator=None):
        self.builder = pygubu.Builder(translator)
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: pygubu.builder.widgets.dialog = (
            self.builder.get_object("aboutdialog", master)
        )
        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def on_gpl3_clicked(self, event=None):
        pass

    def on_mit_clicked(self, event=None):
        pass

    def on_moreinfo_clicked(self, event=None):
        pass

    def on_ok_execute(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = AboutDialogUI(root)
    app.run()
