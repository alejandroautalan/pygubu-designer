#!/usr/bin/python3
import pathlib
import pygubu


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "scrolledtext_demo.ui"


class ScrolledtextDemoApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object("toplevel1", master)
        self.text1 = builder.get_object("stext1")
        self.text2 = builder.get_object("stext2")
        self._populate_text()

        builder.connect_callbacks(self)

    def _populate_text(self):
        filename = PROJECT_PATH / "scrolledtextdemoapp.py"
        with open(filename, "r") as file:
            content = file.read()
            self.text1.insert("0.0", content)
            self.text2.insert("0.0", content)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = ScrolledtextDemoApp()
    app.run()
