import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "settingsdemo.ui"


class SettingsDialog:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object("settingsdialog", master)

        self.iconsizevar = None
        self.langvar = None
        self.winposvar = None
        builder.import_variables(self, ["iconsizevar", "langvar", "winposvar"])

        builder.connect_callbacks(self)

        # Init settings
        self.iconsizevar.set("24px")
        self.langvar.set("Spanish")
        self.winposvar.set(False)

    def run(self):
        self.mainwindow.run()

    def on_cancel(self):
        self.mainwindow.destroy()

    def on_close(self, event):
        self.on_cancel()

    def on_save(self):
        print("Save settings here:")
        print("iconsizevar", self.iconsizevar.get())
        print("langvar", self.langvar.get())
        print("winposvar", self.winposvar.get())
        print("Settings saved.")
        self.mainwindow.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsDialog(root)
    app.run()
