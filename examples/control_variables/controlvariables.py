#!/usr/bin/python3
import pathlib
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "controlvariables.ui"


class MyApplication:
    def __init__(self, master=None):
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file(PROJECT_UI)

        # 3: Create the main window
        self.mainwindow = builder.get_object("mainwindow", master)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = MyApplication()
    app.run()
