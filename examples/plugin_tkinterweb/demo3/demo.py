#!/usr/bin/python3
"""
Tkinterweb Notebook demo

A simple demo for Notebook widget.

UI source file: demo_notebook.ui
"""
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
from demoui import DemoAppUI

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demo_notebook.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class DemoApp(DemoAppUI):
    def __init__(self, master=None):
        super().__init__(
            master,
            project_ui=PROJECT_UI,
            resource_paths=RESOURCE_PATHS,
            translator=None,
            on_first_object_cb=None,
        )
        self.builder.connect_callbacks(self)

        self.webview1 = self.builder.get_object("webview1")
        self.webview2 = self.builder.get_object("webview2")
        self.mainwindow.after_idle(self.load_topics)

    def load_topics(self):
        topics = ["topic1.html", "topic2.html"]
        views = [self.webview1, self.webview2]
        for view, topic in zip(views, topics):
            filename = str(PROJECT_PATH / topic)
            view.load_file(filename)


if __name__ == "__main__":
    app = DemoApp()
    app.run()
