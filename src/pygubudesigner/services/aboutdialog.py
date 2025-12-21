#!/usr/bin/python3
import os
import pathlib
import tkinter as tk
import webbrowser
import importlib.metadata as pkgmeta
import pygubu
import pygubudesigner
import pygubudesigner.services.aboutdialogui as baseui

from pygubu.stockimage import StockImage


def image_loader(master, image_name: str):
    return StockImage.get(image_name)


class AboutDialog(baseui.AboutDialogUI):
    def __init__(self, master=None, translator=None):
        super().__init__(
            master, translator=translator, image_loader=image_loader
        )
        pugubu_version = pkgmeta.version("pygubu")
        designer_version = pkgmeta.version("pygubu-designer")
        txt = self.pygubu_version.cget("text")
        txt = txt.replace("%version%", pugubu_version)
        self.pygubu_version.configure(text=txt)
        txt = self.designer_version.cget("text")
        txt = txt.replace("%version%", designer_version)
        self.designer_version.configure(text=txt)

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
