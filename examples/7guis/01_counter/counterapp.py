#!/usr/bin/python3
import pathlib
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "counter.ui"


class CounterApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)

        self.counter_var = None
        builder.import_variables(self, ["counter_var"])

        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def on_count_clicked(self):
        value = self.counter_var.get()
        value += 1
        self.counter_var.set(value)


if __name__ == "__main__":
    app = CounterApp()
    app.run()
