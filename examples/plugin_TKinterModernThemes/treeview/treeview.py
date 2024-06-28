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
        self.treeview_widget = self.builder.get_object("treeview1")

    def run(self):
        self.mainwindow.run()

    def print_selected_cmd(self):
        print("Currently selected:", self.treeview_widget.selection())
        for item in self.treeview_widget.selection():
            print("--", self.treeview_widget.item(item))


if __name__ == "__main__":
    # root = tk.Tk()
    app = App()
    app.run()
