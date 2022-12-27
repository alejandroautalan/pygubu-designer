#!/usr/bin/python3
import pathlib
from tkinter import messagebox
import pygubu


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "pathchooserdemo.ui"


class MyApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(PROJECT_UI)

        self.mainwindow = builder.get_object("mainwindow", master)

        self.path_var = None
        builder.import_variables(self, ["path_var"])

        self.filepath = builder.get_object("filepath")
        self.default_path = pathlib.Path.home() / "default.txt"
        self.filepath.configure(
            path=self.default_path,
            filetypes=[("Python files", ".py"), ("Any", ".*")],
        )
        self.last_dir = None

        self.btn_process = builder.get_object("btn_process")

        builder.connect_callbacks(self)

    def on_path_changed(self, event=None):
        # Get the path choosed by the user
        path = self.path_var.get()
        # or:
        # path = self.filepath.cget("path")  # If you are not using specific tk variable.

        enable_btn = False
        if (
            self.default_path != path
            and pathlib.Path(self.path_var.get()).exists()
        ):
            enable_btn = True

        btn_state = "normal" if enable_btn else "disabled"
        self.btn_process.configure(state=btn_state)

    def on_reset_clicked(self):
        self.last_dir = pathlib.Path(self.path_var.get()).parent
        self.filepath.configure(
            path=self.default_path, initialdir=self.last_dir
        )
        self.btn_process.configure(state="disabled")

    def on_process_clicked(self):
        path = self.path_var.get()
        messagebox.showinfo("You choosed:", path, parent=self.mainwindow)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = MyApp()
    app.run()
