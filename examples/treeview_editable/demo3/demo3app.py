#!/usr/bin/python3
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
from demo3appui import DemoAppUI
from pygubu.widgets.editabletreeview import (
    EditableTreeview,
    _ComboboxEditor,
    _EntryEditor,
)


class EntryPopupIEditor(_EntryEditor):
    """A editor with a popup menu when the <Tab> key is pressed."""

    def _create_widget(self, master, **kw):
        self.other_editor = None
        self.entry: ttk.Entry = super()._create_widget(master, **kw)
        self._create_popup()
        self.entry.bind("<Tab>", self.show_popup)
        return self.entry

    def option_selected(self, value):
        self._variable.set(value)
        if self.other_editor is not None:
            self.other_editor.category_changed(value)

    def _create_popup(self):
        self.popmenu = tk.Menu(self.entry, tearoff=0)
        options = ("A", "B", "C", "D")
        for option in options:
            self.popmenu.add_command(
                label=option, command=lambda o=option: self.option_selected(o)
            )

    def show_popup(self, event=None):
        try:
            x, y = self.entry.winfo_rootx(), self.entry.winfo_rooty()
            self.popmenu.tk_popup(x, y, 0)
            self.entry.wait_window(self.popmenu)
        except Exception as e:
            print(e)


class OtherIEditor(_EntryEditor):
    """A custom editor "connected" to another."""

    def category_changed(self, value):
        self._variable.set(f"Category changed to: {value}")


class CountryIEditor(_ComboboxEditor):
    """A country combobox conecteable with a city combobox editor."""

    def _create_widget(self, master, **kw):
        kw["state"] = "readonly"
        self.combo_city = None
        self.combo = super()._create_widget(master, **kw)
        self.combo.bind("<<ComboboxSelected>>", self.on_country_changed)
        return self.combo

    def on_country_changed(self, event=None):
        if self.combo_city is None:
            return
        self.combo_city.country_changed(self.value)


class CityIEditor(_ComboboxEditor):
    """A city combobox editor."""

    city_map = None

    def _create_widget(self, master, **kw):
        kw["state"] = "readonly"
        self.combo = super()._create_widget(master, **kw)
        return self.combo

    def update_cities(self, country):
        if country not in self.city_map:
            return
        cities = self.city_map[country]["cities"]
        self.combo.configure(values=cities)

    def country_changed(self, country):
        self.update_cities(country)
        self._variable.set("")


country_data = {
    "Argentina": {
        "cities": [
            "Cordoba",
            "Jujuy",
            "Santa Fe",
            "Santiago del Estero",
            "Otra",
        ],
    },
    "Peru": {
        "cities": ["Lima", "Arequipa", "Trujillo", "Otra"],
    },
    "Paraguay": {
        "cities": ["Asunción", "Concepción", "Villarrica", "Otra"],
    },
}

country_names = [name for name in country_data.keys()]

table_data = [
    ["0001", "Alex", "Argentina", "Cordoba"],
    ["0002", "Ivana", "Paraguay", "Asunción"],
    ["0003", "Mario", "Peru", "Lima"],
]


class DemoApp(DemoAppUI):
    def __init__(self, master=None):
        super().__init__(master)
        self.county_editor = None
        self.city_editor = None

        self.etv: EditableTreeview = self.builder.get_object("etv")
        self.allow_edit.set(True)

        # Create and connect the editors
        CityIEditor.city_map = country_data
        self.county_editor = CountryIEditor(self.etv)
        self.county_editor.combo.configure(
            values=[name for name in country_data.keys()]
        )
        self.city_editor = CityIEditor(self.etv)
        self.county_editor.combo_city = self.city_editor

        self.entry_popup_editor = EntryPopupIEditor(self.etv)
        self.other_editor = OtherIEditor(self.etv)
        self.entry_popup_editor.other_editor = self.other_editor

        self._setup_data()

    def _setup_data(self):
        # Add some data to the treeview
        for row in table_data:
            self.etv.insert("", tk.END, text=row[0], values=row[1:])

    def on_cell_edited(self, event=None):
        # This method is connected with the <<TreeviewCellEdited>>
        # virtual event of the Editabletreeview
        col, item = self.etv.get_event_info()
        msg = f"Column {col} of item {item} was changed"
        print(msg)

        # Test get_value method
        print(f"Column '{col}' value: ", self.etv.get_value(col, item))

    def on_editors_unfocused(self, event=None):
        pass

    def on_inplace_edit(self, event=None):
        # Allow edition only if allow_edit variable is checked
        if not self.allow_edit.get():
            return

        # Get the column id and item id of the cell
        # that is going to be edited
        col, item = self.etv.get_event_info()

        # Define the widget editor to be used to edit the column value
        if col in ("col_person",):
            self.etv.inplace_entry(col, item)
        if col == "col_country":
            self.etv.inplace_editor(col, item, self.county_editor)
        if col == "col_city":
            country = self.etv.get_value("col_country", item)
            self.city_editor.update_cities(country)
            self.etv.inplace_editor(col, item, self.city_editor)
        if col == "col_category":
            self.etv.inplace_editor(col, item, self.entry_popup_editor)
        if col == "col_other":
            self.etv.inplace_editor(col, item, self.other_editor)

    def on_row_selected(self, event=None):
        pass


if __name__ == "__main__":
    app = DemoApp()
    app.run()
