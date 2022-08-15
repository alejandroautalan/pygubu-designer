#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import pathlib
import pygubu
from pygubu.widgets.editabletreeview import InplaceEditor

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demoapp.ui"


class CustomInplaceEditor(InplaceEditor):
    """Example of a custom cell editor for an Editabletreeview

    Subclass from InplaceEditor and implement the methods:

    @property
    def widget(self) -> tk.Widget:
        ...

    @property
    def value(self):
        ...

    def edit(self, value) -> None:
        ...
    """

    def __init__(self, master):
        self._notify_blocked = False
        self._widget = frame = ttk.Frame(master)
        self._label = ttk.Label(frame, width=5, anchor=tk.E)
        self._label.pack(side=tk.LEFT)
        self._scale = ttk.Scale(
            frame, from_=10, to=100, command=self._onscalechange
        )
        self._scale.pack(side=tk.LEFT, fill=tk.X)

    def _onscalechange(self, value):
        strval = f"{float(value):.2f}"
        self._label.configure(text=strval)
        # Notify treeview that value was changed
        if not self._notify_blocked:
            self._notify_change()

    def focus_set(self) -> None:
        self._scale.focus_set()

    @property
    def widget(self) -> tk.Widget:
        return self._widget

    @property
    def value(self):
        value = self._scale.get()
        return round(value, 2)

    def edit(self, value) -> None:
        self._notify_blocked = True
        self._scale.set(value)
        self._label.configure(text=value)
        self._notify_blocked = False


class EditableTreeviewDemoApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object("toplevel1", master)
        self.etv = builder.get_object("etv")

        self.allow_edit = None
        builder.import_variables(self, ["allow_edit"])
        self.allow_edit.set(True)

        builder.connect_callbacks(self)

        self.combo_values = ("A", "B", "C", "D", "E", "F")
        self.custom_editor = None
        self._setup_data()

    def _setup_data(self):

        # Add some data to the treeview
        data = [
            ("news", "http://www.realnews.com.ar", True, "A", 0, 10),
            ("games", "https://www.gogamer.com.ar", True, "F", 0, 20),
            ("search", "https://duckduckgo.com.ar", False, "D", 0, 30),
        ]
        for d in data:
            self.etv.insert("", tk.END, text=d[0], values=d[1:])

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
            if col in ("col1",):
                self.etv.inplace_entry(col, item)
            if col == "col2":
                self.etv.inplace_checkbutton(col, item)
            if col == "col3":
                self.etv.inplace_combobox(
                    col,
                    item,
                    self.combo_values,
                    readonly=True,
                    update_values=False,
                )
            if col == "col4":
                self.etv.inplace_spinbox(col, item, 0, 100, 5)
            if col == "col5":
                # create editor here, so all editors are created in order.
                if self.custom_editor is None:
                    self.custom_editor = CustomInplaceEditor(self.etv)
                self.etv.inplace_editor(col, item, self.custom_editor)

    def on_row_selected(self, event=None):
        # This method is connected with the <<TreeviewSelect>> event
        # The Editabletreeview also uses this event so, Do not forget to
        # mark Add=True in the binding definition

        sel = self.etv.selection()
        if sel:
            item = sel[0]
            print(f"Row item {item} was selected.")


if __name__ == "__main__":
    app = EditableTreeviewDemoApp()
    app.run()
