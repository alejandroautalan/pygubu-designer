#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from demoui import DemoAppUI


class DemoApp(DemoAppUI):
    def __init__(self, master=None):
        super().__init__(master)
        self.web_frame = self.builder.get_object("web_frame")
        self.web_frame.on_url_change(self.on_url_change)
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

    def on_url_change(self, url):
        """Process URL changed event from HtmlFrame"""
        self.url_var.set(url)


if __name__ == "__main__":
    app = DemoApp()
    app.run()
