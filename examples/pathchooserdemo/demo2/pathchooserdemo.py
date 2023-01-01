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

        self.source_file_var = None
        self.source_dir_var = None
        self.output_file_var = None
        self.output_dir_var = None
        builder.import_variables(
            self,
            [
                "source_file_var",
                "source_dir_var",
                "output_file_var",
                "output_dir_var",
            ],
        )

        file_types = [("Python files", ".py"), ("Any", ".*")]

        self.source_file = builder.get_object("pc_source_file")
        self.source_file.configure(filetypes=file_types)

        self.output_file = builder.get_object("pc_output_file")
        self.default_output_file = pathlib.Path.home() / "default.txt"
        self.output_file.configure(
            path=self.default_output_file,
            filetypes=file_types,
        )
        self.output_dir = builder.get_object("pc_output_dir")
        self.default_output_dir = pathlib.Path.home() / "tmp"
        self.output_dir.configure(path=self.default_output_dir)

        self.btn_process = builder.get_object("btn_process")

        builder.connect_callbacks(self)

    def on_path_changed(self, event=None):
        inputs = (
            self.source_file_var.get(),
            self.source_dir_var.get(),
            self.output_file_var.get(),
            self.output_dir_var.get(),
        )

        enable_btn = True if all(inputs) else False
        btn_state = "normal" if enable_btn else "disabled"
        self.btn_process.configure(state=btn_state)

    def on_reset_clicked(self):
        self.source_dir.configure(path="")
        self.source_file.configure(path="")
        self.output_dir.configure(path=self.default_output_dir)
        self.output_file.configure(path=self.default_output_file)
        self.btn_process.configure(state="disabled")

    def on_process_clicked(self):
        msg = f"""
        Source File: {self.source_file_var.get()}
        Source Dir: {self.source_dir_var.get()}

        Output File: {self.output_file_var.get()}
        Output Dir: {self.output_dir_var.get()}
        """
        messagebox.showinfo("You choosed:", msg, parent=self.mainwindow)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = MyApp()
    app.run()
