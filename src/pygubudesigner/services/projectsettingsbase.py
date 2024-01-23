#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "project_settings.ui"


class ProjectSettingsBase:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("settingsdialog", master)
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def on_template_change(self, event=None):
        pass

    def on_style_browse(self):
        pass

    def on_style_remove(self):
        pass

    def on_style_new(self):
        pass

    def btn_cancel_clicked(self):
        pass

    def btn_apply_clicked(self):
        pass

    def on_dialog_close(self, event=None):
        pass

    def btn_cwadd_clicked(self):
        pass

    def btn_cwremove_clicked(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectSettingsBase(root)
    app.run()
