#!/usr/bin/python3
import pathlib
from tkinter import messagebox
import pygubu


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "menu.ui"


class MyApplication:
    def __init__(self, master=None):
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file(PROJECT_UI)

        # 3: Create the widget using self.master as parent
        self.mainwindow = builder.get_object("mainwindow", master)

        # Set main menu
        self.mainmenu = builder.get_object("mainmenu", self.mainwindow)
        self.mainwindow.configure(menu=self.mainmenu)

        # Configure callbacks
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def on_mfile_item_clicked(self, itemid):
        if itemid == "mfile_open":
            messagebox.showinfo("File", "You clicked Open menuitem")

        if itemid == "mfile_quit":
            messagebox.showinfo("File", "You clicked Quit menuitem. Byby")
            self.mainwindow.quit()

    def on_about_clicked(self):
        messagebox.showinfo(
            "About", "You clicked About menuitem", parent=self.mainwindow
        )


if __name__ == "__main__":
    app = MyApplication()
    app.run()
