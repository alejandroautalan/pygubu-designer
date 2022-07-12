#!/usr/bin/python3
import pathlib
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "image_property.ui"


class MyApplication:
    def __init__(self, master=None):
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file(PROJECT_UI)

        # 3: Set images path before creating any widget
        builder.add_resource_path(PROJECT_PATH)

        # 4: Create the widget using self.master as parent
        self.mainwindow = builder.get_object("mainwindow", master)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = MyApplication()
    app.run()
