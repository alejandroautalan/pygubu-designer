#!/usr/bin/python3
import random
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demo.ui"


class DemoApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Tk = builder.get_object("tk1", master)
        builder.connect_callbacks(self)

        self.filter_var: tk.StringVar = None
        builder.import_variables(self)

        self.tree = builder.get_object("treeview")
        self.companies = [
            "Acme Corporation",
            "Globex Corporation",
            "Soylent Corp",
            "Initech",
            "Umbrella Corporation",
            "Hooli",
            "Vehement Capital Partners",
            "Massive Dynamic",
            "Storm Solutions",
            "Business Mosaics Ltd",
        ]
        self.sectors = ["A", "B", "C", "D"]
        self.names = [
            "Alejandro",
            "Alejo",
            "Alendo",
            "Alesio",
            "Alessandro",
            "Alessio",
            "Alex",
            "Alexander",
            "Fabricio",
            "Fabrizio",
            "Facundo",
            "Joel",
            "Lautaro",
            "Marco",
        ]
        self._build_tree()

    def _build_tree(self):
        random.seed(1020304)
        for c in self.companies:
            itemid = self.tree.insert("", "end", text=c)
            sector_count = len(self.sectors)
            for sid in random.sample(
                self.sectors, k=random.randint(0, sector_count - 1)
            ):
                sname = f"Sector {sid}"
                sitem = self.tree.insert(itemid, "end", text=sname)
                for pname in random.sample(self.names, k=random.randint(0, 4)):
                    self.tree.insert(sitem, "end", text=pname)

    def run(self):
        self.mainwindow.mainloop()

    def _walk_tree(self, rootitem="", level=0):
        if rootitem != "":
            pad = " " * (level + 1)
            text = self.tree.item(rootitem, "text")
            line = f"{pad}{rootitem} {text}"
            print(line)
        for item in self.tree.get_children(rootitem):
            self._walk_tree(item, level + 1)

    def on_do_filter(self, event=None):
        self.tree.filter_by(self.filter_var.get())

    def on_print_all(self):
        self.tree.filter_remove(remember=True)
        self._walk_tree()
        self.tree.filter_restore()

    def on_print_results(self):
        if self.tree.filter_active:
            self._walk_tree()
        else:
            print("No filter")

    def on_filter_remove(self):
        self.filter_var.set("")
        self.tree.filter_remove()


if __name__ == "__main__":
    app = DemoApp()
    app.run()
