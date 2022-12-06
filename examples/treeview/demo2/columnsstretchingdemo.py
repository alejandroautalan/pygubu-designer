#!/usr/bin/python3
import pathlib
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "columns_stretching.ui"


class ColumnsStretchingDemo:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel2", master)
        builder.connect_callbacks(self)

        # Connect treeview2 with scrollbars
        hsb = self.builder.get_object("tv2_hsb")
        vsb = self.builder.get_object("tv2_vsb")
        tv2 = self.builder.get_object("treeview2")

        vsb.configure(command=tv2.yview)
        tv2.configure(yscrollcommand=vsb.set)

        hsb.configure(command=tv2.xview)
        tv2.configure(xscrollcommand=hsb.set)
        # End of scrollbars configuration

        # Load data
        self.load_data()

    def load_data(self):
        data = [
            ["Mercury", 4_879, 58.66, 88, 179, "rocky", 0, "5 months"],
            ["Venus", 12_104, 243, 224, 482, "rocky", 0, "3 months"],
            ["Earth", 12_756, 1, 365.25, 15, "rocky", "1m", "-"],
            ["Mars", 6_756, 1.03, 687, -63, "rocky", "2m", "8 months"],
            [
                "Jupiter",
                142_984,
                0.42,
                4_332,
                -121,
                "gaseous",
                "60m + rings",
                "5 years",
            ],
            [
                "Saturn",
                120_536,
                0.45,
                10_775,
                -125,
                "gaseous",
                "31m + rings",
                "7 years",
            ],
            [
                "Uranus",
                51_118,
                0.71,
                30_681,
                -193,
                "gaseous",
                "27m + rings",
                "10 years",
            ],
            [
                "Neptune",
                49_528,
                0.67,
                60_193,
                -173,
                "gaseous",
                "13m + rings",
                "12 years",
            ],
        ]
        tv1 = self.builder.get_object("treeview1")
        tv2 = self.builder.get_object("treeview2")
        tv3 = self.builder.get_object("treeview3")
        for line in data:
            tv1.insert("", "end", text=line[0], values=line[1:])
            tv2.insert("", "end", text=line[0], values=line[1:])
            tv3.insert("", "end", text=line[0], values=line[1:])

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = ColumnsStretchingDemo()
    app.run()
