#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

from i18n import translator

# Set translatable strings marker
_ = translator

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demo-i18n.ui"


class DemoI18NApp:
    def __init__(self, master=None, translator=None):
        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Tk = builder.get_object("tk1", master)
        builder.connect_callbacks(self)

        self.countries = [
            _("Argentina"),
            _("Brazil"),
            _("Peru"),
            _("Spain"),
            _("Germany"),
            _("Belgium"),
            _("Finland"),
            _("Other"),
        ]
        self.cb_country = self.builder.get_object("cb_country")
        self.cb_country.configure(values=self.countries)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = DemoI18NApp(translator=translator)
    app.run()
