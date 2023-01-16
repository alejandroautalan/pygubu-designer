#!/usr/bin/python3
import pathlib
import tkinter as tk
from tkinter import ttk
from testnewiconsapp import TestnewiconsApp


class MainApp(TestnewiconsApp):
    def __init__(self, master=None):
        super().__init__(master)
        self.file_list: ttk.Treeview = self.builder.get_object("file_list")
        self.lbl_128 = self.builder.get_object("lbl_128")
        self.lbl_64 = self.builder.get_object("lbl_64")
        self.lbl_32 = self.builder.get_object("lbl_32")
        self.lbl_24 = self.builder.get_object("lbl_24")
        self.lbl_16 = self.builder.get_object("lbl_16")
        self.img_bag = []
        self.dir_chooser = self.builder.get_object("dir_chooser")
        self.dir_chooser.configure(path=pathlib.Path.cwd())

    def on_reload_clicked(self):
        self.on_dir_selected()

    def on_dir_selected(self, event=None):
        self.file_list.delete(*self.file_list.get_children())
        path = pathlib.Path(self.images_dir_var.get())
        if not path.exists():
            return
        file_list = []
        for file in path.glob("*"):
            if file.suffix in (".png", ".svg"):
                file_list.append(file)
        file_list.sort()
        for file in file_list:
            self.file_list.insert("", "end", text=f"{file.name}")

    def on_file_selected(self, event=None):
        print("on_file_selected")
        item = self.file_list.selection()[0]
        name = self.file_list.item(item, "text")
        filename = pathlib.Path(self.images_dir_var.get()) / name
        labels = (
            self.lbl_128,
            self.lbl_64,
            self.lbl_32,
            self.lbl_24,
            self.lbl_16,
        )
        sizes = (128, 64, 32, 24, 16)
        self.img_bag = []
        if filename.suffix == ".svg":
            for label, size in zip(labels, sizes):
                options = f"svg -scaletowidth {size}"
                img = tk.PhotoImage(file=filename, format=options)
                self.img_bag.append(img)
                label.configure(image=img)
        elif filename.suffix == ".png":
            img_base = None
            for label, size in zip(labels, sizes):
                if size == 128:
                    img = tk.PhotoImage(file=filename)
                    img_base = img
                    self.img_bag.append(img)
                    label.configure(image=img)
                    sizew = img.width()
                    if sizew < 128:
                        break
                    else:
                        continue
                factor = int(img_base.width() / size)
                img = img_base.subsample(factor)
                self.img_bag.append(img)
                label.configure(image=img)


if __name__ == "__main__":
    app = MainApp()
    app.run()
