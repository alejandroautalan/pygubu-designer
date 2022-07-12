#!/usr/bin/python3
import pathlib
import pygubu


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "timer_main.ui"


class MyApplication:
    def __init__(self, master=None):
        builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object("mainwindow", master)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = MyApplication()
    app.run()
