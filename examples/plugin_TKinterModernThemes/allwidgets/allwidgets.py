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
        self.var_radiobutton.trace_add("write", self.printradiobuttons)
        self.var_textinput.trace_add("write", self.textupdate)
        self.var_spinboxnum.set(25)
        self.var_slider.set(25)

    def run(self):
        self.mainwindow.run()

    def printcheckboxvars(self, number):
        print("Checkbox number:", number, "was pressed")
        print(
            "Checkboxes: ", self.var_checkbox1.get(), self.var_checkbox2.get()
        )

    def printradiobuttons(self, _var, _indx, _mode):
        print("Radio button: ", self.var_radiobutton.get(), "pressed.")

    def textupdate(self, _var, _indx, _mode):
        print("Current text status:", self.var_textinput.get())

    def optionmenu_clicked(self, value):
        print(f"Option menu clicked, option: {value}")

    def validateText(self, arg1, text):
        if self == self:
            pass
        if "q" not in text:
            return True
        print("The letter q is not allowed.")
        return False

    def handleButtonClick(self):
        print(
            "Button clicked. Current toggle button state: ",
            self.var_togglebutton.get(),
        )


if __name__ == "__main__":
    # root = tk.Tk()
    # theme = input("Theme (azure / park / sun-valley): ").lower()
    # mode = input("dark / light: ").lower()
    app = App()
    app.run()
