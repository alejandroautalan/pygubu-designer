#!/usr/bin/python3
import pathlib
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "tempconv.ui"


class TempconvApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)

        self.tempc_var = None
        self.tempf_var = None
        builder.import_variables(self, ["tempc_var", "tempf_var"])

        builder.connect_callbacks(self)

        self.tempc = builder.get_object("tempc")
        self.tempf = builder.get_object("tempf")

    def run(self):
        self.mainwindow.mainloop()

    def calculate_celsius(self, f):
        celsius = (f - 32) * (5 / 9)
        celsius = f"{celsius:.2f}"
        self.tempc_var.set(celsius)

    def calculate_fahrenheit(self, c):
        fahrenheit = c * (9 / 5) + 32
        fahrenheit = f"{fahrenheit:.2f}"
        self.tempf_var.set(fahrenheit)

    def temp_validate(self, d_action, p_entry_value, w_entry_name):
        is_valid = True
        if d_action == "1":  # Insert
            try:
                temperature = float(p_entry_value)
                widget = self.mainwindow.nametowidget(w_entry_name)
                if widget is self.tempc:
                    self.calculate_fahrenheit(temperature)
                else:
                    self.calculate_celsius(temperature)
            except ValueError:
                is_valid = False
        return is_valid


if __name__ == "__main__":
    app = TempconvApp()
    app.run()
