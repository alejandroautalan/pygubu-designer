# encoding: utf8
import pathlib
from tkinter import messagebox
import pygubu


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "button_cb.ui"


class Myapp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(PROJECT_UI)

        self.mainwindow = builder.get_object("mainwindow", master)

        builder.connect_callbacks(self)

        callbacks = {"on_button2_clicked": self.on_button2_clicked}

        builder.connect_callbacks(callbacks)

    def on_my_button_clicked(self):
        messagebox.showinfo(
            "From callback", "My button was clicked !!", parent=self.mainwindow
        )

    def on_button2_clicked(self):
        messagebox.showinfo(
            "From callback", "Button 2 was clicked !!", parent=self.mainwindow
        )

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = Myapp()
    app.run()
