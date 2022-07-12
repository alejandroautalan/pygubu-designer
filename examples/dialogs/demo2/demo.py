#!/usr/bin/python3
import pathlib
import time
import tkinter as tk

import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demo.ui"


class DemoApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("mainwindow", master)
        builder.connect_callbacks(self)

        self.progressdialog = builder.get_object(
            "progressdialog", self.mainwindow
        )

        # Show data load at start
        self.mainwindow.after(100, self.show_load_dialog)

    def show_load_dialog(self):
        self.progressdialog.run()
        self.load_data()

    def load_data(self):
        tv = self.builder.get_object("treeview1")
        pb = self.builder.get_object("progressbar1")
        pb.start()
        for i in range(1, 101):
            # simulate work, sleep 1/10 seconds
            time.sleep(0.1)
            tv.insert("", tk.END, text="item {0}".format(i))

            # update windows
            self.mainwindow.update()
        self.progressdialog.close()

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = DemoApp()
    app.run()
