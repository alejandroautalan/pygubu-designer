#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demo2.ui"


class Demo2App:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Toplevel = builder.get_object("toplevel1", master)

        self.allow_edit: tk.BooleanVar = None
        builder.import_variables(self)

        builder.connect_callbacks(self)

        self.allow_edit.set(True)
        self.combo_values = ("blue", "green", "red", "yellow", "white", "black")
        self.etv = builder.get_object("etv")
        self._setup_data()

    def _setup_data(self):

        # Add some data to the treeview
        data = [
            ("uid", "uniqueid", True),
            ("size", 200, True),
            (
                "color",
                "red",
                False,
            ),
        ]
        for d in data:
            self.etv.insert("", tk.END, iid=d[0], text=d[0], values=d[1:])

    def run(self):
        self.mainwindow.mainloop()

    def on_cell_edited(self, event=None):
        # This method is connected with the <<TreeviewCellEdited>>
        # virtual event of the Editabletreeview
        col, item = self.etv.get_event_info()
        msg = f"Column {col} of item {item} was changed"
        print(msg)
        data = self.etv.item(item, "values")
        print("New values:", data)

        # Test get_value method
        print(f"Column '{col}' value: ", self.etv.get_value(col, item))

    def on_editors_unfocused(self, event=None):
        # user clicked in treeview area with no rows
        # the editors where hidden.
        print("Editors hidden")

    def on_inplace_edit(self, event=None):
        # This method is connected with the <<TreeviewInplaceEdit>>
        # virtual event of the Editabletreeview
        #
        # Get the column id and item id of the cell
        # that is going to be edited
        col, item = self.etv.get_event_info()

        # Allow edition only if allow_edit variable is checked
        if self.allow_edit.get():
            # Define the widget editor to be used to edit the column value
            # Now you can use diferent editors in same column for
            # diferent item ids
            print(col, item)
            if item == "uid":
                return
            if col == "col_value":
                if item == "size":
                    self.etv.inplace_spinbox(col, item, 1, 1000, 5)
                elif item == "color":
                    self.etv.inplace_combobox(
                        col,
                        item,
                        self.combo_values,
                        readonly=True,
                        update_values=False,
                    )
            if col == "col_active":
                self.etv.inplace_checkbutton(col, item)

    def on_row_selected(self, event=None):
        # This method is connected with the <<TreeviewSelect>> event
        # The Editabletreeview also uses this event so, Do not forget to
        # mark Add=True in the binding definition

        sel = self.etv.selection()
        if sel:
            item = sel[0]
            print(f"Row item {item} was selected.")


if __name__ == "__main__":
    app = Demo2App()
    app.run()
