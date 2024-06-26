#!/usr/bin/python3
import pathlib
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "simple_demo.ui"


class SimpleDemoApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("ctk1", master)

        self.radiobutton_var = None
        builder.import_variables(self, ["radiobutton_var"])

        builder.connect_callbacks(self)

        self.progressbar_1 = builder.get_object("progressbar_1")
        self.slider_1 = builder.get_object("slider_1")
        self.optionmenu_1 = builder.get_object("optionmenu_1")
        self.combobox_1 = builder.get_object("combobox_1")

        # Init values
        self.slider_1.set(0.5)
        self.optionmenu_1.set("CTkOptionMenu")
        self.combobox_1.set("CTkComboBox")
        self.radiobutton_var.set(1)

    def run(self):
        self.mainwindow.mainloop()

    def button_callback(self):
        print("Button click", self.combobox_1.get())

    def slider_callback(self, value):
        self.progressbar_1.set(value)


if __name__ == "__main__":
    app = SimpleDemoApp()
    app.run()
