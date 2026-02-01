#!/usr/bin/python3
"""
Tkinterweb HtmlFrame demo

A simple demo for HtmlFrame widget.

Requires tkinterweb > 4.0

UI source file: demo_frame.ui
"""
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
from demoui import DemoAppUI

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demo_frame.ui"
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

        self.web_frame = self.builder.get_object("web_frame")
        self.file_chooser = self.builder.get_object("file_chooser")
        file_types = [("HTML files", ".html .htm"), ("Any", ".*")]
        self.file_chooser.configure(filetypes=file_types)

    def on_btn_load_clicked(self):
        """Process click of load/play button."""
        self.on_user_enters_url()

    def on_user_enters_url(self, event=None):
        """Process <Key-Return> binding."""
        self.web_frame.load_website(self.url_var.get())

    def on_file_choosed(self, event=None):
        """Process <<PathChooserPathChanged>> event."""
        path = self.file_chooser.cget("path")
        self.on_url_change("file://" + path)
        self.web_frame.load_file(path)

    def on_url_change(self, event=None):
        """Process URL changed event from HtmlFrame"""
        self.url_var.set(self.web_frame.current_url)


if __name__ == "__main__":
    app = DemoApp()
    app.run()
