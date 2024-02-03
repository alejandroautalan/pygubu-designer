#!/usr/bin/python3
import os
import pathlib
import tkinter as tk
import webbrowser
import pygubu
import pygubudesigner
import pygubudesigner.services.aboutdialogui as base

from pygubu.stockimage import StockImage
from pygubudesigner.preferences import DATA_DIR

IMAGE_DIR = DATA_DIR / "images" / "images-gif"
if tk.TkVersion >= 8.6:
    IMAGE_DIR = DATA_DIR / "images" / "images-png"

base.PROJECT_PATH = DATA_DIR / "ui"
base.PROJECT_UI = DATA_DIR / "ui" / "about_dialog.ui"
base.RESOURCE_PATHS = [IMAGE_DIR]

# Uncomment line for testing this file only
# StockImage.register_all_from_dir(IMAGE_DIR)


class AboutDialog(base.AboutDialogUI):
    def __init__(self, master=None, translator=None):
        super().__init__(master, translator)
        entry = self.builder.get_object("version")
        txt = entry.cget("text")
        txt = txt.replace("%version%", str(pygubu.__version__))
        entry.configure(text=txt)
        entry = self.builder.get_object("designer_version")
        txt = entry.cget("text")
        txt = txt.replace("%version%", str(pygubudesigner.__version__))
        entry.configure(text=txt)

    def run(self):
        self.mainwindow.run()

    def on_gpl3_clicked(self, event=None):
        url = "https://www.gnu.org/licenses/gpl-3.0.html"
        webbrowser.open_new_tab(url)

    def on_mit_clicked(self, event=None):
        url = "https://opensource.org/licenses/MIT"
        webbrowser.open_new_tab(url)

    def on_moreinfo_clicked(self, event=None):
        url = "https://github.com/alejandroautalan/pygubu-designer"
        webbrowser.open_new_tab(url)

    def on_ok_execute(self):
        self.mainwindow.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = None

    def create_dialog():
        app = AboutDialog(root)
        app.run()

    root.after(1000, create_dialog)
    root.mainloop()
