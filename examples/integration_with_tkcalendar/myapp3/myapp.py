#!/usr/bin/python3
import pathlib
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "main.ui"


class MyApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object("mainwindow", master)

        self.date_entry = builder.get_object("dateentry1")

        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def on_date_selected(self, event=None):
        date = self.date_entry.get_date()
        print(f"User selected date: {date} ({type(date)})")


if __name__ == "__main__":
    app = MyApp()
    app.run()
