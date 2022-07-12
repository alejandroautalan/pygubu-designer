#!/usr/bin/python3
import pathlib
from tkinter import messagebox
import pygubu


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "pathchooserdemo.ui"


class MyApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(PROJECT_UI)

        self.mainwindow = builder.get_object("mainwindow", master)
        self.filepath = builder.get_object("filepath")

        builder.connect_callbacks(self)

    def on_path_changed(self, event=None):
        # Get the path choosed by the user
        path = self.filepath.cget("path")
        # show the path
        messagebox.showinfo("You choosed:", path, parent=self.mainwindow)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = MyApp()
    app.run()
