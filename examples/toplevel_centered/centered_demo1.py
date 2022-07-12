#!/usr/bin/python3
import pathlib
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demo.ui"


class CenteredDemoApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object("topmain", master)
        builder.connect_callbacks(self)

        # center window on screen after creation
        self._first_init = True
        self.mainwindow.bind("<Map>", self.center_window)

    def center_window(self, event):
        if self._first_init:
            print("centering window...")
            toplevel = self.mainwindow
            height = toplevel.winfo_height()
            width = toplevel.winfo_width()
            x_coord = int(toplevel.winfo_screenwidth() / 2 - width / 2)
            y_coord = int(toplevel.winfo_screenheight() / 2 - height / 2)
            geom = f"{width}x{height}+{x_coord}+{y_coord}"
            toplevel.geometry(geom)
            self._first_init = False

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = CenteredDemoApp()
    app.run()
