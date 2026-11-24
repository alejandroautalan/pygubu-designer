#!/usr/bin/python3
import logging
import tkinter as tk
from tkinter import ttk

from pygubu import builder
from pygubu.stockimage import StockImage
from pygubu.widgets.simpletooltip import create as create_tooltip

import pygubudesigner.services.widgets.properties_editorui as baseui
from pygubudesigner.i18n import translator as _
from pygubudesigner.properties.editors import create_editor
from pygubudesigner.properties.manager import (
    PropertiesManager,
    PropertyRegistry,
)

logger = logging.getLogger(__name__)
CLASS_MAP = builder.CLASS_MAP


class PropertiesEditorMixin:
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._current = None
        self._prop_bag = {}
        self._sep = None  # separator

    def get_properties_frame(self):
        pass

    def _create_properties(self, in_frame, row_start: int = 0, col_start: int = 0):
        self._sep = ttk.Separator(in_frame)

        for name in PropertiesManager.iter_names():
            self._create_editor_slot(in_frame, name)

        self._redisplay_slots(in_frame, row_start, col_start)

    def _redisplay_slots(self, _in_frame, row_start: int = 0, col_start: int = 0):
        """Redo layout of editor slots ordered by property name."""
        row = row_start
        col = col_start

        label: ttk.Label = None
        widget: tk.Widget = None
        for name in PropertiesManager.iter_names():
            label, widget = self._prop_bag[name]
            is_visible = widget.winfo_ismapped()
            label.grid(row=row, column=col, sticky=tk.EW, pady="2p")
            widget.grid(row=row, column=col + 1, sticky=tk.EW, pady="2p")

            if not is_visible:
                label.grid_remove()
                widget.grid_remove()

            row += 1
            if name == "id":
                self._sep.grid(
                    row=row, column=col, sticky=tk.EW, pady="2p", columnspan=2
                )
                row += 1

    def _create_editor_slot(self, in_frame, name):
        label_tpl = "{0}:"
        kwdata = PropertiesManager.get_definition(name)
        labeltext = label_tpl.format(name)
        label = ttk.Label(in_frame, text=labeltext, anchor=tk.W)
        # label.grid(row=row, column=col, sticky=tk.EW, pady="2p")
        label.tooltip = create_tooltip(label, "?")
        widget = self._create_editor(in_frame, name, kwdata)
        # widget.grid(row=row, column=col + 1, sticky=tk.EW, pady="2p")
        # row += 1
        self._prop_bag[name] = (label, widget)
        logger.debug("Created property: %s", name)

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
        final_mode = params["mode"]
        if final_mode is None:
            msg = (
                "Configuration ERROR. "
                + "Unable to determine editor mode for '%s.%s' property."
            )
            logger.warning(msg, classname, pname)
            params["mode"] = "entry"
        logger.debug("Setting editor mode for %s", pname)
        editor.parameters(**params)

        # Setup tooltip
        editor_help = pdescr.get("help", None)
        editor_help = _("No help defined.") if editor_help is None else editor_help
        if isinstance(editor_help, dict):
            found_match = False
            for k, v in editor_help.items():
                if classname.startswith(k):
                    editor_help = v
                    found_match = True
                    break
            # NOTE: review this process for custom properties.
            if not found_match:
                editor_help = ""  # No help string found
        label.tooltip.text = editor_help

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

        for name in PropertiesManager.iter_names():
            label, widget = self._prop_bag[name]
            if name in ("class", "id") or name in class_descr.properties:
                self.update_editor(label, widget, wdescr, name)
                label.grid()
                widget.grid()
            else:
                # hide property widget
                label.grid_remove()
                widget.grid_remove()

    def hide_all(self):
        """Hide all properties from property editor."""
        self.current = None

        for _v, (label, widget) in self._prop_bag.items():
            label.grid_remove()
            widget.grid_remove()


# i18n - Setup yout translator function
baseui.i18n_translator = _

#
# image loader configuration


def image_loader(image_name):
    return StockImage.get(image_name)


baseui.image_loader = image_loader


#
# Manual user code
#


class PropertiesEditor(PropertiesEditorMixin, baseui.PropertiesEditorUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        # Wait until all properties definitions are loaded,
        # then create property editors.
        self.after_idle(self.load_properties_later)

        self._redisplay_cb = None

    def on_new_property_defined(self, _sender, name):
        """Create new editor slot and schedules a redisplay."""
        self._create_editor_slot(self.fprop, name)

        if self._redisplay_cb is None:
            self._redisplay_cb = self.after_idle(self.redisplay_properties)

    def redisplay_properties(self):
        self._redisplay_slots(self.fprop)
        self._redisplay_cb = None

    def load_properties_later(self):
        self._create_properties(self.fprop)
        self.hide_all()

        # Connect to the registry for additional property definitions.
        PropertyRegistry.on_property_new.connect(self.on_new_property_defined)


if __name__ == "__main__":
    root = tk.Tk()
    test_widget = PropertiesEditor(root)
    test_widget.pack(expand=True, fill="both")
    root.mainloop()
