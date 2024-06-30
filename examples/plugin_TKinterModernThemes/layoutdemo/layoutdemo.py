#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from layoutdemoui import AppUI


class App(AppUI):
    def __init__(self, master=None):
        super().__init__(master)

    def run(self):
        self.mainwindow.run()


if __name__ == "__main__":
    # root = tk.Tk()
    app = App()
    app.run()
