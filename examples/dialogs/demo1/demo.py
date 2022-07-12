#!/usr/bin/python3
import pathlib
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demo.ui"


class DemoApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("top", master)

        self.dialog1 = builder.get_object("dialog1", self.mainwindow)
        self.dialog2 = builder.get_object("dialog2", self.mainwindow)

        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def on_btn1_click(self):
        self.dialog1.run()

    def on_btn2_click(self):
        self.dialog2.run()

    def on_dialog1_close(self, event=None):
        # captures <<DialogClose>> Binding event
        self.dialog1.close()

    def on_dialog2_close(self, event=None):
        # captures <<DialogClose>> Binding event
        self.dialog2.close()

    def on_dialog2_close_clicked(self):
        # dialog 2 close button action.
        self.dialog2.close()


if __name__ == "__main__":
    app = DemoApp()
    app.run()
