import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu

from settingsdialog import SettingsDialog


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "settingsdemo.ui"


class SettingsdemoApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object("mainwindow", master)
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def on_quit(self):
        self.mainwindow.quit()

    def on_show_settings(self):
        # Create dialog window.
        dialog = SettingsDialog(self.mainwindow)
        dialog.run()
        # Dialog was configured to run in modal state.
        # So wait until the window is closed.
        self.mainwindow.wait_window(dialog.mainwindow.toplevel)


if __name__ == "__main__":
    app = SettingsdemoApp()
    app.run()
