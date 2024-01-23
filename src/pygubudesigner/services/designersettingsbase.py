#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "designer_settings.ui"


class DesignerSettingsBase:
    def __init__(self, master=None, translator=None):
        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("preferences", master)
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def btn_cancel_cliced(self):
        pass

    def btn_apply_clicked(self):
        pass

    def on_dialog_close(self, event=None):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = DesignerSettingsBase(root)
    app.run()
