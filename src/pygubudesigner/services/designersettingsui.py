#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "designer_settings.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class DesignerSettingsUI:
    def __init__(self, master=None, translator=None):
        self.builder = pygubu.Builder(translator)
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: pygubu.builder.widgets.dialog = (
            self.builder.get_object("preferences", master)
        )
        self.builder.connect_callbacks(self)

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
    app = DesignerSettingsUI(root)
    app.run()
