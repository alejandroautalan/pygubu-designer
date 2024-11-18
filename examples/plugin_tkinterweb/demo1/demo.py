#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from demoui import DemoAppUI


class DemoApp(DemoAppUI):
    def __init__(self, master=None):
        super().__init__(master)


if __name__ == "__main__":
    app = DemoApp()
    app.run()
