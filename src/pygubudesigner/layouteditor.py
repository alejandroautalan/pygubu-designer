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

import logging
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from pygubu import builder
from pygubu.widgets.simpletooltip import create as create_tooltip

from pygubudesigner import properties
from pygubudesigner.containerlayouteditor import ContainerLayoutEditor
from pygubudesigner.i18n import translator as _
from pygubudesigner.propertieseditor import PropertiesEditor
from pygubudesigner.widgets.propertyeditor import LayoutManagerPropertyEditor

logger = logging.getLogger(__name__)
CLASS_MAP = builder.CLASS_MAP


class LayoutEditor(PropertiesEditor):
    managers_keys = ("grid", "pack", "place")
    managers_labels = (_("Grid"), _("Pack"), _("Place"))
    managers = dict(zip(managers_keys, managers_labels))

    def _create_properties(self):
        """Populate a frame with a list of all editable properties"""

        # To mantain container options:
        self._container_options = {}

        # Layout Options editors
        self._rcbag = {}  # bag for row/column prop editors
        # main options frame
        # self._fprop = fprop = ttk.Labelframe(self._sframe.innerframe,
        #                                     text=_('Options:'), padding=4)
        self._fprop = fprop = ttk.Frame(self._sframe.innerframe)
        fprop.grid(row=0, sticky="nswe")

        # Layout selector
        label = ttk.Label(fprop, text=_("Manager:"))
        label.grid(row=0, column=0, sticky=tk.EW, pady=2)
        self.layout_selector = combo = LayoutManagerPropertyEditor(fprop)
        combo.parameters(state="readonly", values=self.managers)
        combo.grid(row=0, column=1, sticky=tk.EW, pady=2)
        combo.bind("<<PropertyChanged>>", self._layout_manager_changed)
        self._allowed_managers = self.managers.keys()
        # Separator
        w = ttk.Separator(fprop, orient="horizontal")
        w.grid(row=1, column=0, columnspan=2, sticky="ew", pady=4)

        # Other Layout properties
        label_tpl = "{0}:"
        row = 2
        col = 0

        self._groups = (
            ("00", properties.MANAGER_PROPERTIES, properties.LAYOUT_OPTIONS),
        )

        for gcode, plist, propdescr in self._groups:
            for name in plist:
                kwdata = propdescr[name]
                labeltext = label_tpl.format(name)
                label = ttk.Label(self._fprop, text=labeltext, anchor=tk.W)
                label.grid(row=row, column=col, sticky=tk.EW, pady=2)
                label.tooltip = create_tooltip(label, "?")
                widget = self._create_editor(self._fprop, name, kwdata)
                widget.grid(row=row, column=col + 1, sticky=tk.EW, pady=2)
                row += 1
                self._propbag[gcode + name] = (label, widget)

        # container layout editor
        self._cleditor = ContainerLayoutEditor(self._sframe.innerframe)
        self._cleditor.grid(row=1, sticky="nswe", pady="5 0")

    def edit(self, wdescr, manager_options, container_options=None):
        self._current = wdescr

        # need to save the container info when updating the view.
        # this function is called again in _layout_manager_changed
        if container_options is not None:
            self._container_options = container_options

        wclass = wdescr.classname
        # class_descr = CLASS_MAP[wclass].builder
        max_children = CLASS_MAP[wclass].builder.maxchildren
        max_children = 0 if max_children is None else max_children
        is_container = CLASS_MAP[wclass].builder.container
        layout_required = CLASS_MAP[wclass].builder.layout_required
        allow_container_layout = CLASS_MAP[wclass].builder.container_layout
        show_layout = layout_required

        # manager selector
        manager = wdescr.manager
        manager_prop = properties.GRID_PROPERTIES
        if manager == "pack":
            manager_prop = properties.PACK_PROPERTIES
        elif manager == "place":
            manager_prop = properties.PLACE_PROPERTIES

        if show_layout:
            self._fprop.grid()
            self._allowed_managers = manager_options
            self.layout_selector.edit(manager)

            # layout properties
            for gcode, proplist, gproperties in self._groups:
                for name in proplist:
                    propdescr = gproperties[name]
                    label, widget = self._propbag[gcode + name]
                    if show_layout and name in manager_prop:
                        self.update_editor(
                            label, widget, wdescr, name, propdescr
                        )
                        label.grid()
                        widget.grid()
                    else:
                        label.grid_remove()
                        widget.grid_remove()
        else:
            self._fprop.grid_remove()

        # determine if show container layout options
        has_children = self._container_options.get("has_children", False)
        children_grid_dim = self._container_options.get("grid_dim", None)

        if is_container and allow_container_layout and has_children:
            self._cleditor.grid()
            cmanager = wdescr.container_manager
            self._cleditor.edit(wdescr, cmanager, children_grid_dim)
        else:
            self._cleditor.grid_remove()

        self._sframe.reposition()

    def _layout_manager_changed(self, event=None):
        if self._current is None:
            # I'm not editing anything
            return

        old_manager = self._current.manager
        new_manager = self.layout_selector.value
        needs_container_change = new_manager not in self._allowed_managers

        if needs_container_change:
            self.layout_selector.edit(old_manager)

            def cb(f=old_manager, t=new_manager):
                return self._ask_manager_change(f, t)

            self._sframe.after_idle(cb)
        else:
            self._current.manager = new_manager
            self.edit(self._current, self._allowed_managers)

            # If we're moving away from grid, remove the row/col values
            # in the treeview (so the user knows grid is not being used)
            if old_manager == "grid":
                self._sframe.event_generate("<<ClearSelectedGridTreeInfo>>")

    def _ask_manager_change(self, old_manager, new_manager):
        title = _("Change Manager")
        msg = _("Change manager from {0} to {1}?").format(
            old_manager, new_manager
        )
        detail = _("All container widgets will be updated.")
        user_accepts_change = messagebox.askokcancel(
            title,
            msg,
            detail=detail,
            parent=self.layout_selector.winfo_toplevel(),
        )
        if user_accepts_change:
            topack = "<<LayoutEditorContainerManagerToPack>>"
            togrid = "<<LayoutEditorContainerManagerToGrid>>"
            event_name = togrid if new_manager == "grid" else topack
            self._sframe.event_generate(event_name)

    def _on_property_changed(self, name, editor):
        value = editor.value
        # Save new value and update the preview
        self._current.layout_property(name, value)

    def update_editor(self, label, editor, wdescr, pname, propdescr):
        pdescr = propdescr.copy()
        manager = wdescr.manager

        if manager in pdescr:
            pdescr = dict(pdescr, **pdescr[manager])

        label.tooltip.text = pdescr.get("help", None)
        params = pdescr.get("params", {})
        editor.parameters(**params)
        default = pdescr.get("default", "")

        value = wdescr.layout_property(pname)
        if not value and default:
            value = default
        editor.edit(value)

    def hide_all(self):
        super().hide_all()
        self._fprop.grid_remove()
        self._cleditor.grid_remove()
