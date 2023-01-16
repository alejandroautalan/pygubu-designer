#!/usr/bin/python3
import pathlib
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "testnewicons.ui"


class TestnewiconsApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)

        self.images_dir_var = None
        builder.import_variables(self, ["images_dir_var"])

        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def on_dir_selected(self, event=None):
        pass

    def on_reload_clicked(self):
        pass

    def on_file_selected(self, event=None):
        pass


if __name__ == "__main__":
    app = TestnewiconsApp()
    app.run()
