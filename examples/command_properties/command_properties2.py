#!/usr/bin/python3
# command_properties.py
import pathlib
from tkinter import messagebox
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "command_properties.ui"


class MyApplication:
    def __init__(self, master=None):
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file(PROJECT_UI)

        # 3: Create the widget using self.master as parent
        self.mainwindow = builder.get_object("mainwindow", master)

        # Method 2: Connect callbacks with methods
        # defined in this class
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    # define the method callbacks:

    def on_button1_clicked(self):
        messagebox.showinfo(
            "Message", "You clicked Button 1", parent=self.mainwindow
        )

    def on_button2_clicked(self):
        messagebox.showinfo(
            "Message", "You clicked Button 2", parent=self.mainwindow
        )

    def on_button3_clicked(self):
        messagebox.showinfo(
            "Message", "You clicked Button 3", parent=self.mainwindow
        )


if __name__ == "__main__":
    app = MyApplication()
    app.run()
