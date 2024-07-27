#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from radiobuttonui import RadiobuttonAppUI


class RadiobuttonApp(RadiobuttonAppUI):
    def __init__(self, master=None):
        super().__init__(master)


if __name__ == "__main__":
    app = RadiobuttonApp()
    app.run()
