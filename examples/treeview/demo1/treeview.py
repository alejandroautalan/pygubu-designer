# encoding: utf8
import pathlib
import tkinter as tk
from tkinter import messagebox
from random import randint
import pygubu


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "treeview.ui"


class Myapp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object("mainwindow", master)

        self.tv = builder.get_object("treeview")
        self.populate_tree()

        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def _add_tree(self, name, parent=""):
        column_values = (
            f"Column value for item {name}",  # column 1
            randint(0, 100),  # Hidden column value
        )
        self.tv.insert(parent, tk.END, text=name, values=column_values)

    def populate_tree(self):
        for index in range(1, 20):
            name = f"Item {index}"
            self._add_tree(name)

    def on_row_selected(self, event=None):
        print(event)
        sel = self.tv.selection()
        if sel:
            item = sel[0]
            values = self.tv.item(item, "values")
            print("Hidden col value:", values[1])

    def on_treecolumn_click(self):
        messagebox.showinfo(
            "From callback", "Tree column clicked !!", parent=self.mainwindow
        )


if __name__ == "__main__":
    app = Myapp()
    app.run()
