#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from treeviewui import AppUI


resources = {
    "tree_data": [
        {"fruit": "apple"},
        {"fruit": "orange"},
        {"fruit": "lemon"},
    ],
    "tree_data2": [
        {
            "fruit": "apple",
            "color": "red",
            "open": True,
            "subdata": [{"fruit": "pear"}],
        },
        {
            "fruit": "orange",
            "color": "orange",
            "open": False,
            "subdata": [{"fruit": "pear"}],
        },
        {"fruit": "lemon"},
    ],
}


class App(AppUI):
    def __init__(self, master=None):
        super().__init__(master, data_pool=resources)

    def run(self):
        self.mainwindow.run()


if __name__ == "__main__":
    # root = tk.Tk()
    app = App()
    app.run()
