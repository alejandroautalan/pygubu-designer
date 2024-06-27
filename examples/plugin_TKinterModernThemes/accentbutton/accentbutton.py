#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from accentbuttonui import AppUI


class App(AppUI):
    def __init__(self, master=None):
        super().__init__(master)

    def run(self):
        self.mainwindow.run()

    def handle_btn_click(self):
        print("Button Clicked!")


if __name__ == "__main__":
    # root = tk.Tk()
    # app = App(root)
    app = App()
    app.run()
