#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from dialog1ui import SimpleDialog1UI


class SimpleDialog1(SimpleDialog1UI):
    def __init__(self, master=None):
        super().__init__(master)

    def run(self):
        # call the dialog run function
        self.mainwindow.run()

    def on_dialog_close(self):
        # The main window does not destroy de dialog,
        # so here just hide de dialog
        self.mainwindow.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleDialog1(root)
    app.run()
