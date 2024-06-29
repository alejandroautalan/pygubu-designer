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
        self.var_checkbox1.set(True)
        self.var_textinput.set("Type text here.")
        self.var_spinboxcolor.set("blue")
        # self.var_combobox.set("")

    def run(self):
        self.mainwindow.run()

    def printcheckboxvars(self, number):
        print("Checkbox number:", number, "was pressed")
        print(
            "Checkboxes: ", self.var_checkbox1.get(), self.var_checkbox2.get()
        )

    def optionmenu_clicked(self, value):
        print(f"Option menu clicked, option: {value}")


if __name__ == "__main__":
    # root = tk.Tk()
    app = App()
    app.run()
