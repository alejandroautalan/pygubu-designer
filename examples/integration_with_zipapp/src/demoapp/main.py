#!/usr/bin/python3
import pathlib
import pygubu
import importlib.resources as resources

PROJECT_PKG = "demoapp"
PROJECT_UI = resources.files(PROJECT_PKG) / "data" / "demoapp.ui"


class DemoAppBase:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()

        # Tell builder to search images in package.
        builder.add_resource_package(PROJECT_PKG)

        # Load ui file from resources
        builder.add_from_file(PROJECT_UI.open("rb"))

        # Main widget
        self.mainwindow = builder.get_object("mainwindow", master)
        builder.connect_callbacks(self)

        # Load extra additional text from resources:
        text_file = resources.files(PROJECT_PKG) / "data" / "info.txt"
        text_content = text_file.read_text()
        text2 = builder.get_object("text2")
        text2.insert("0.0", text_content)

    def run(self):
        self.mainwindow.mainloop()


def run():
    app = DemoAppBase()
    app.run()


if __name__ == "__main__":
    run()
