#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

import pygubudesigner.services.messageboxui as base
from pygubudesigner.preferences import DATA_DIR


base.PROJECT_PATH = DATA_DIR / "ui"
base.PROJECT_UI = base.PROJECT_PATH / "messagebox.ui"


class CustomMessageBox(base.CustomMessageBoxUI):
    def __init__(self, master=None):
        super().__init__(master)

    def run(self):
        self.mainwindow.run()

    def configure(self, title=None, message=None, detail=None):
        pass


def show_error(master, title=None, message=None, detail=None):
    dialog = CustomMessageBox(master)
    dialog.run()


if __name__ == "__main__":
    root = tk.Tk()

    def create_dialog():
        app = CustomMessageBox(root)
        app.run()

    root.after(1000, create_dialog)
    root.mainloop()
