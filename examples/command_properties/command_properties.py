#!/usr/bin/python3
# command_properties.py
import pathlib
from tkinter import messagebox
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "command_properties.ui"

#
# define the function callbacks
#


def on_button1_click():
    messagebox.showinfo("Message", "You clicked Button 1")


def on_button2_click():
    messagebox.showinfo("Message", "You clicked Button 2")


def on_button3_click():
    messagebox.showinfo("Message", "You clicked Button 3")


class MyApplication:
    def __init__(self, master=None):
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file(PROJECT_UI)

        # 3: Create the mainwindow
        self.mainwindow = builder.get_object("mainwindow", master)

        # Method 1 Configure callbacks with functions
        callbacks = {
            "on_button1_clicked": on_button1_click,
            "on_button2_clicked": on_button2_click,
            "on_button3_clicked": on_button3_click,
        }

        builder.connect_callbacks(callbacks)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = MyApplication()
    app.run()
