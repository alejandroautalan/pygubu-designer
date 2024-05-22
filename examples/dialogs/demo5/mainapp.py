#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from mainappui import MyDemoAppUI
from dialog1 import SimpleDialog1


class MyDemoApp(MyDemoAppUI):
    def __init__(self, master=None):
        super().__init__(master)

        self.dialog = SimpleDialog1(self.mainwindow)

    def on_fullscreen_clicked(self):
        value = self.fullscreen_var.get()
        self.mainwindow.wm_attributes("-fullscreen", value)

    def on_showmodal_clicked(self):
        dialog_in_fullscreen = self.dialog_fullscreen_var.get()
        dialog_top = self.dialog.mainwindow.toplevel
        dialog_top.wm_attributes("-fullscreen", dialog_in_fullscreen)

        self.dialog.run()


if __name__ == "__main__":
    app = MyDemoApp()
    app.run()
