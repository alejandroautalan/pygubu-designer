import os
import pygubu
import pathlib

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demoapp.ui"


class DemoApp:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        print(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('topdemo')
        builder.connect_callbacks(self)
        
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = DemoApp()
    app.run()

