#
# Copyright 2012-2022 Alejandro Autalán
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import tkinter as tk
import tkinter.ttk as ttk

from pygubu.widgets.simpletooltip import create as create_tooltip

from pygubudesigner import properties
from pygubudesigner.widgetdescr import WidgetMeta
from pygubudesigner.widgets.containerlayouteditorbase import (
    ContainerLayoutEditorBase,
)
from pygubudesigner.widgets.gridselector import GridRCselectorWidget
from pygubudesigner.widgets.propertyeditor import create_editor
from pygubudesigner.i18n import _


class ContainerLayoutEditor(ContainerLayoutEditorBase):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        # Add grid selector
        self.gridselector = w = GridRCselectorWidget(self.rcselectorframe)
        w.bind("<<Gridselector:CellSelected>>", self._on_gridcell_clicked)
        w.pack()

        self._propbag = {}
        self._rcbag = {}
        self._current = None
        self._mainpanel_label = _("Options for {0} container")
        self._rowpanel_label = _("Row index: {0}")
        self._colpanel_label = _("Column index: {0}")
        self._build_editors()

    def _build_editors(self):
        # layout properties
        label_tpl = "{0}:"
        row = col = 0
        groups = (
            (
                "00",
                properties.CONTAINER_MANAGER_PROPERTIES,
                properties.LAYOUT_OPTIONS,
            ),
        )

        for gcode, plist, propdescr in groups:
            for name in plist:
                kwdata = propdescr[name]
                labeltext = label_tpl.format(name)
                label = ttk.Label(self.foptions, text=labeltext, anchor=tk.W)
                label.grid(row=row, column=col, sticky=tk.EW, pady=2)
                tooltip_text = kwdata.get("help", None)
                label.tooltip = create_tooltip(label, tooltip_text)
                alias = f"cprop_{name}"
                widget = self._create_editor(self.foptions, alias, kwdata)
                widget.grid(row=row, column=col + 1, sticky=tk.EW, pady=2)
                row += 1
                self._propbag[gcode + name] = (label, widget)

        # Row/Column Editors
        fgr = self.rowframe
        name_format = "row_{0}"  # row_{name}
        row = 0
        label_tpl = "{0}:"
        for pname in properties.GRID_RC_PROPERTIES:
            kwdata = properties.LAYOUT_OPTIONS[pname]
            alias = name_format.format(pname)
            labeltext = label_tpl.format(pname)
            label = ttk.Label(fgr, text=labeltext, anchor=tk.W)
            label.grid(row=row, column=0, sticky=tk.EW, pady=2)
            tooltip_text = kwdata.get("help", None)
            label.tooltip = create_tooltip(label, tooltip_text)

            widget = self._create_editor(fgr, alias, kwdata)
            widget.grid(row=row, column=1, sticky=tk.EW, pady=2)
            self._rcbag[alias] = (label, widget)
            row = row + 1
        fgr.columnconfigure(1, weight=1)

        fgc = self.colframe
        name_format = "col_{0}"  # row_{name}
        row = 0
        label_tpl = "{0}:"
        for pname in properties.GRID_RC_PROPERTIES:
            kwdata = properties.LAYOUT_OPTIONS[pname]
            alias = name_format.format(pname)
            labeltext = label_tpl.format(pname)
            label = ttk.Label(fgc, text=labeltext, anchor=tk.W)
            label.grid(row=row, column=0, sticky=tk.EW, pady=2)
            tooltip_text = kwdata.get("help", None)
            label.tooltip = create_tooltip(label, tooltip_text)

            widget = self._create_editor(fgc, alias, kwdata)
            widget.grid(row=row, column=1, sticky=tk.EW, pady=2)
            self._rcbag[alias] = (label, widget)
            row = row + 1
        fgc.columnconfigure(1, weight=1)

    def _create_editor(self, master, pname, wdata):
        editor = None
        wtype = wdata.get("editor", None)

        # I don't have class name at this moment
        # so setup class specific values on update_property_widget
        editor = create_editor(wtype, master)

        def make_on_change_cb(pname, editor):
            def on_change_cb(event):
                self._on_property_changed(pname, editor)

            return on_change_cb

        editor.bind("<<PropertyChanged>>", make_on_change_cb(pname, editor))
        return editor

    def update_editor(self, label, editor, wdescr, pname, propdescr):
        pdescr = propdescr.copy()
        manager = wdescr.container_manager

        if manager in pdescr:
            pdescr = dict(pdescr, **pdescr[manager])

        params = pdescr.get("params", {})
        editor.parameters(**params)
        default = pdescr.get("default", "")

        value = wdescr.container_property(pname)
        if not value and default:
            value = default
        editor.edit(value)

    def update_rc_editor(
        self, type_, index, label, editor, wdescr, pname, propdescr
    ):
        pdescr = propdescr.copy()
        classname = wdescr.classname

        if classname in pdescr:
            pdescr = dict(pdescr, **pdescr[classname])

        params = pdescr.get("params", {})
        editor.parameters(**params)
        default = pdescr.get("default", "")

        value = ""
        value = wdescr.gridrc_property(type_, str(index), pname)
        if not value and default:
            value = default
        editor.edit(value)

    def _btn_indexall_clicked(self):
        self.gridselector.selection_clear()
        self._edit_grid_cell("all", "all")

    def _btn_clearall_clicked(self):
        if self._current:
            self._current.gridrc_clear()
            self._edit_gridrc()

    def _on_property_changed(self, alias, editor):
        if alias.startswith("cprop_"):
            # Contaner grid property
            __, pname = alias.split("_")
            self._current.container_property(pname, editor.value)
        else:
            # It's a grid RC change
            rowcol, pname = alias.split("_")
            index = 0 if rowcol == "row" else 1
            if self.gridselector.selection is None:
                number = "all"
            else:
                number = str(self.gridselector.selection[index])
            target = self._current
            target.gridrc_property(rowcol, number, pname, editor.value)

            # update grid view
            self.gridselector.mark_clear_all()
            self.gridselector.mark_grid_rows(False)
            self.gridselector.mark_grid_cols(False)

            for row in self._current.gridrc_row_indexes():
                if row == "all":
                    self.gridselector.mark_grid_rows()
                else:
                    self.gridselector.mark_row(int(row))
            for col in self._current.gridrc_column_indexes():
                if col == "all":
                    self.gridselector.mark_grid_cols()
                else:
                    self.gridselector.mark_column(int(col))

            # Update the preview now, after the grid rc changes have been made.
            target.notify("LAYOUT_GRIDRC_CHANGED", target)

    def _on_gridcell_clicked(self, event=None):
        self._edit_grid_cell(*self.gridselector.selection)

    def _edit_grid_cell(self, row, col):
        # Update RC properties editors for cell
        target = self._current
        for key in self._rcbag:
            rowcol, name = key.split("_")
            propdescr = properties.LAYOUT_OPTIONS[name]
            index = col if rowcol == "col" else row
            label, widget = self._rcbag[key]
            self.update_rc_editor(
                rowcol, index, label, widget, target, name, propdescr
            )
        # update labels
        label = self._rowpanel_label.format(row)
        self.rowframe_label.configure(text=label)
        label = self._colpanel_label.format(col)
        self.colframe_label.configure(text=label)

    def _edit_gridrc(self):
        # wdescr = self._current
        self.gridrcpanel.grid()
        self.gridselector.set_dim(*self._grid_dim)
        self.gridselector.mark_clear_all()
        self.gridselector.mark_grid_rows(False)
        self.gridselector.mark_grid_cols(False)
        self.gridselector.select_cell(0, 0)

        for row in self._current.gridrc_row_indexes():
            if row == "all":
                self.gridselector.mark_grid_rows()
            else:
                self.gridselector.mark_row(int(row))
        for col in self._current.gridrc_column_indexes():
            if col == "all":
                self.gridselector.mark_grid_cols()
            else:
                self.gridselector.mark_column(int(col))

    def edit(self, wdescr, manager, grid_dim=None):
        self._current = wdescr
        self._grid_dim = (1, 1) if grid_dim is None else grid_dim

        txt_label = self._mainpanel_label.format(str(manager).capitalize())
        self.lbl_title.configure(text=txt_label)

        manager_prop = properties.CONTAINER_GRID_PROPERTIES
        if manager == "pack":
            manager_prop = properties.CONTAINER_PACK_PROPERTIES

        # layout properties
        groups = (
            (
                "00",
                properties.CONTAINER_MANAGER_PROPERTIES,
                properties.LAYOUT_OPTIONS,
            ),
        )

        for gcode, proplist, gproperties in groups:
            for name in proplist:
                propdescr = gproperties[name]
                label, widget = self._propbag[gcode + name]
                if name in manager_prop:
                    self.update_editor(label, widget, wdescr, name, propdescr)
                    label.grid()
                    widget.grid()
                else:
                    label.grid_remove()
                    widget.grid_remove()

        self.gridrcpanel.grid_remove()
        if manager == "grid":
            self._edit_gridrc()


if __name__ == "__main__":
    root = tk.Tk()
    widget = ContainerLayoutEditor(root)
    widget.pack(expand=True, fill="both")

    wd = WidgetMeta("tk.Frame", "frame1")
    wd.gridrc_property("row", "0", "minsize", "25")
    wd.gridrc_property("col", "0", "minsize", "125")

    wd.gridrc_property("row", "0", "minsize", "25")
    wd.gridrc_property("col", "2", "minsize", "125")

    wd.gridrc_property("row", "3", "minsize", "5")
    wd.gridrc_property("col", "2", "minsize", "75")

    print(wd)
    widget.edit(wd, "grid", (10, 10))
    # widget.edit(wd, 'pack')

    root.mainloop()
