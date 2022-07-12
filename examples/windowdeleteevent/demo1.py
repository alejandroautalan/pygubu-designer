#!/usr/bin/python3
import pathlib
import pygubu


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demo1.ui"


class Application:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object("mainwindow", master)

        # Connect Delete event to toplevel window
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.on_close_window)

    def on_close_window(self, event=None):
        print(event)
        print("On close window")

        # Since we are capturing the WM_DELETE_WINDOW
        # we need to close de window manually.

        # Call destroy on toplevel to finish program
        self.mainwindow.destroy()

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = Application()
    app.run()
