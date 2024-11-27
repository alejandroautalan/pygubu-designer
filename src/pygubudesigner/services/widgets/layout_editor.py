#!/usr/bin/python3
import logging
import tkinter as tk
import tkinter.ttk as ttk

from tkinter import messagebox

from pygubu import builder
from pygubu.widgets.simpletooltip import create as create_tooltip
from pygubu.stockimage import StockImage

from pygubudesigner import properties
from pygubudesigner.i18n import translator as _
from pygubudesigner.propertieseditor import PropertiesEditorMixin
import pygubudesigner.services.widgets.layout_editorui as baseui

logger = logging.getLogger(__name__)
CLASS_MAP = builder.CLASS_MAP

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

toolbar_expand_config = dict(
    expand_reset=dict(
        pack=dict(expand="", fill=""),
        grid=dict(sticky=""),
        place=dict(relwidth="", relheight=""),
    ),
    expand_all=dict(
        pack=dict(expand="True", fill="both"),
        grid=dict(sticky="nsew"),
        place=dict(relwidth="1", relheight="1"),
    ),
    expand_width=dict(
        pack=dict(expand="True", fill="x"),
        grid=dict(sticky="ew"),
        place=dict(relwidth="1", relheight=""),
    ),
    expand_height=dict(
        pack=dict(expand="True", fill="y"),
        grid=dict(sticky="ns"),
        place=dict(relwidth="", relheight="1"),
    ),
)


class LayoutEditor(PropertiesEditorMixin, baseui.LayoutEditorUI):
    managers_keys = ("grid", "pack", "place")
    managers_labels = (_("Grid"), _("Pack"), _("Place"))
    managers = dict(zip(managers_keys, managers_labels))

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        # To mantain container options:
        self._container_options = {}

        # Layout Options editors
        self._rcbag = {}  # bag for row/column prop editors

        self._create_properties(self.fprop)
        self.hide_all()

    def _create_properties(self, in_frame, row_start=0, col_start=0):
        """Populate a frame with a list of all editable properties"""

        # Layout selector
        self.layout_selector.parameters(state="readonly", values=self.managers)
        self.layout_selector.bind(
            "<<PropertyChanged>>", self._layout_manager_changed
        )
        self._allowed_managers = self.managers.keys()

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
                label = ttk.Label(in_frame, text=labeltext, anchor=tk.W)
                label.grid(row=row, column=col, sticky=tk.EW, pady=2)
                label.tooltip = create_tooltip(label, "?")
                widget = self._create_editor(in_frame, name, kwdata)
                widget.grid(row=row, column=col + 1, sticky=tk.EW, pady=2)
                row += 1
                self._prop_bag[gcode + name] = (label, widget)

    def edit(
        self,
        wdescr,
        manager_options,
        container_options=None,
        parent_classname=None,
    ):
        self._current = wdescr

        # need to save the container info when updating the view.
        # this function is called again in _layout_manager_changed
        if container_options is not None:
            self._container_options = container_options

        parent_cancels_children_layout = False
        if parent_classname is not None:
            parent_bo = CLASS_MAP[parent_classname].builder
            parent_cancels_children_layout = parent_bo.children_layout_override
        wclass = wdescr.classname
        # class_descr = CLASS_MAP[wclass].builder
        max_children = CLASS_MAP[wclass].builder.maxchildren
        max_children = 0 if max_children is None else max_children
        is_container = CLASS_MAP[wclass].builder.container
        layout_required = CLASS_MAP[wclass].builder.layout_required
        allow_container_layout = CLASS_MAP[wclass].builder.container_layout
        show_layout = layout_required and not parent_cancels_children_layout

        # manager selector
        manager = wdescr.manager
        manager_prop = properties.GRID_PROPERTIES
        if manager == "pack":
            manager_prop = properties.PACK_PROPERTIES
        elif manager == "place":
            manager_prop = properties.PLACE_PROPERTIES

        if show_layout:
            self.ftoolbar.grid()
            self.fprop.grid()
            self._allowed_managers = manager_options
            self.layout_selector.edit(manager)

            # layout properties
            for gcode, proplist, gproperties in self._groups:
                for name in proplist:
                    propdescr = gproperties[name]
                    label, widget = self._prop_bag[gcode + name]
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
            self.fprop.grid_remove()

        # determine if show container layout options
        # has_children = self._container_options.get("has_children", False)
        children_grid_dim = self._container_options.get("grid_dim", None)

        if is_container and allow_container_layout:  # and has_children:
            self.cleditor.grid()
            cmanager = wdescr.container_manager
            self.cleditor.edit(wdescr, cmanager, children_grid_dim)
        else:
            self.cleditor.grid_remove()

        self.sframe.reposition()

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

            self.after_idle(cb)
        else:
            self._current.manager = new_manager
            self.edit(self._current, self._allowed_managers)

            # If we're moving away from grid, remove the row/col values
            # in the treeview (so the user knows grid is not being used)
            if old_manager == "grid":
                self.sframe.event_generate("<<ClearSelectedGridTreeInfo>>")

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
            self.event_generate(event_name)

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
        self.ftoolbar.grid_remove()
        self.fprop.grid_remove()
        self.cleditor.grid_remove()

    def btn_expand_clicked(self, widget_id):
        if self._current is None:
            return

        gcode = "00"
        manager = self.layout_selector.value
        config = toolbar_expand_config[widget_id][manager]
        for pname, value in config.items():
            editor = self._prop_bag[gcode + pname][1]
            editor.edit(value)
            self._current.layout_property(pname, value)


if __name__ == "__main__":
    root = tk.Tk()
    widget = LayoutEditor(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
