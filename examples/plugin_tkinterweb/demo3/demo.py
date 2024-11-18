#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from demoui import DemoAppUI, PROJECT_PATH


class DemoApp(DemoAppUI):
    def __init__(self, master=None):
        super().__init__(master)
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
