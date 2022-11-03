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

from pygubu import builder
from pygubu.widgets.simpletooltip import create as create_tooltip

from pygubudesigner.i18n import translator as _
from pygubudesigner.widgets.propertyeditor import create_editor
from .widgets import NamedIDPropertyEditor
from .stylehandler import StyleHandler
from pygubudesigner.properties.manager import PropertiesManager

logger = logging.getLogger(__name__)
CLASS_MAP = builder.CLASS_MAP


class PropertiesEditor:
    def __init__(self, frame, **kw):
        self._current = None
        self._sframe = frame
        self._frame = None
        self._propbag = {}
        self._create_properties()

        # Used for refreshing/re-populating the styles combobox.
        # Used when the style definition gets updated (simulates clicking on the treeview item again.)
        reselect_item_func = kw.get("reselect_item_func", None)

        self.style_handler = StyleHandler(
            self._sframe, reselect_item_func=reselect_item_func
        )
        self.style_handler.start_monitoring()

        self.hide_all()

    def _create_properties(self):
        """Populate a frame with a list of all editable properties"""
        self._frame = f = ttk.Frame(self._sframe.innerframe)
        f.grid(sticky="nswe")

        label_tpl = "{0}:"
        row = 0
        col = 0

        for name in PropertiesManager.iternames():
            kwdata = PropertiesManager.get_definition(name)
            labeltext = label_tpl.format(name)
            label = ttk.Label(self._frame, text=labeltext, anchor=tk.W)
            label.grid(row=row, column=col, sticky=tk.EW, pady=2)
            label.tooltip = create_tooltip(label, "?")
            widget = self._create_editor(self._frame, name, kwdata)
            widget.grid(row=row, column=col + 1, sticky=tk.EW, pady=2)
            row += 1
            self._propbag[name] = (label, widget)
            logger.debug("Created property: %s", name)
            if name == "id":
                sep = ttk.Separator(self._frame)
                sep.grid(
                    row=row, column=col, sticky=tk.EW, pady=2, columnspan=2
                )
                row += 1

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

    def _on_property_changed(self, name, editor):
        self._current.widget_property(name, editor.value)

    def update_editor(self, label, editor, wdescr, pname):
        classname = wdescr.classname
        pdescr = PropertiesManager.get_definition_for(pname, classname)

        # Setup name placeholder
        params = pdescr["params"]
        if pname == "id" and params["mode"] == "namedid":
            params["placeholder"] = wdescr.start_id

        # Configure editor
        editor.parameters(**params)

        # Setup tooltip
        help = pdescr.get("help", None)
        if isinstance(help, dict):
            found_match = False
            for k, v in help.items():
                if classname.startswith(k):
                    help = v
                    found_match = True
                    break
            # FIXME: review this process for custom properties.
            if not found_match:
                help = ""  # No help string found
        label.tooltip.text = help

        # setup default value
        default = pdescr.get("default", "")
        value = wdescr.widget_property(pname)

        if not value and default:
            value = default
        editor.edit(value)

    def edit(self, wdescr):
        self._current = wdescr
        wclass = wdescr.classname
        class_descr = CLASS_MAP[wclass].builder

        for name in PropertiesManager.iternames():
            label, widget = self._propbag[name]
            if name in ("class", "id") or name in class_descr.properties:
                self.update_editor(label, widget, wdescr, name)
                label.grid()
                widget.grid()
            else:
                # hide property widget
                label.grid_remove()
                widget.grid_remove()
        self._sframe.reposition()

    def hide_all(self):
        """Hide all properties from property editor."""
        self.current = None

        for _v, (label, widget) in self._propbag.items():
            label.grid_remove()
            widget.grid_remove()
