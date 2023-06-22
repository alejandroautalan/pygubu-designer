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

        # Store function id for later unmapping
        self._center_fid = None

    def center_window(self, event):
        print("centering window...")
        height = self.mainwindow.winfo_height()
        width = self.mainwindow.winfo_width()
        x_coord = int(self.mainwindow.winfo_screenwidth() / 2 - width / 2)
        y_coord = int(self.mainwindow.winfo_screenheight() / 2 - height / 2)
        geom = f"{width}x{height}+{x_coord}+{y_coord}"
        self.mainwindow.geometry(geom)
        # Remove callback
        self.mainwindow.unbind(self._center_fid)
        print("Done centering.")

    def run(self, *, centered=False):
        if centered is True:
            self._center_fid = self.mainwindow.bind('<Map>', self.center_window)        
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = CenteredDemoApp()
    app.run(centered=True)
