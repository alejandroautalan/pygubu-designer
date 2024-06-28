#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
import json
from allwidgetsui import AppUI


# Define treeview data
tree_data = None
with open("treeviewdata.json") as f:
    tree_data = json.load(f)


data = {
    "treeview_json_data": tree_data,
}


class App(AppUI):
    def __init__(self, master=None):
        super().__init__(master, data_pool=data)

    def run(self):
        self.mainwindow.run()


if __name__ == "__main__":
    # root = tk.Tk()
    app = App()
    app.run()
