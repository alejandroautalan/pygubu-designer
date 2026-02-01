#!/usr/bin/python3
"""
Hello world

Very basic hello world example, using *.ui file.

UI source file: helloworld.ui
"""
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
from helloworldui import HelloAppUI

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "helloworld.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class HelloApp(HelloAppUI):
    def __init__(self, master=None):
        # The base class is in charge of doing the following:
        # 1- Create a builder and setup resources path
        # 2- Setup the first object callback.
        # 3- Setup translator
        # 4- Load the indicated UI file
        # 5- Create the mainwindow, calling builder.get_object()
        super().__init__(
            master,
            project_ui=PROJECT_UI,
            resource_paths=RESOURCE_PATHS,
            translator=None,
            on_first_object_cb=None,
        )

        # 6- Finally, yoo call connect callbacks
        self.builder.connect_callbacks(self)


if __name__ == "__main__":
    app = HelloApp()
    app.run()
