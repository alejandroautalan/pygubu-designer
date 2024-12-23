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
import json
import logging
import os
import tkinter as tk
import xml.etree.ElementTree as ET
from collections import Counter, OrderedDict
from functools import partial
from tkinter import messagebox

from pygubu.builder import CLASS_MAP, Builder
from pygubu.component.uidefinition import UIDefinition
from pygubu.stockimage import StockImage, StockImageException

import pygubudesigner
from pygubudesigner import preferences as pref
from pygubudesigner.widgets import EventHandlerEditor
from pygubudesigner.properties.editors import (
    CommandPropertyBase,
    IdentifierPropertyEditor,
    TkVarPropertyEditor,
    NamedIDPropertyEditor,
)

import pygubudesigner.actions as action
from .bindingseditor import BindingsEditor
from .i18n import translator as _
from .propertieseditor import PropertiesEditor
from .util import trlog
from .util.taskexecutor import TaskExecutor
from .widgetdescr import WidgetMeta
from pygubu.forms.widget import FieldWidget
from pygubudesigner.properties.editors.forms import (
    FormFieldNameEntry,
    FormFieldNameSelector,
)
from pygubudesigner.services.project import Project
from pygubu.component.plugin_manager import PluginManager


logger = logging.getLogger("pygubu.designer")


class WidgetsTreeEditor:
    GRID_UP = 0
    GRID_DOWN = 1
    GRID_LEFT = 2
    GRID_RIGHT = 3

    def __init__(self, app):
        self.app = app
        self.treeview = app.treeview
        self.previewer = app.previewer
        self.task_executor = TaskExecutor(app.mainwindow)
        self.treedata = {}
        self.counter = Counter()
        self.virtual_clipboard_for_duplicate = None
        self.duplicating = False
        self.duplicate_parent_iid = None
        self.update_builder = None
        self.update_bo = {}
        self.preview_update_cbid = None
        self.scheduled_widget_updates = []
        # self._stretch_cb = None
        self.treeview.bind("<Configure>", self._on_tree_configure)

        self.treeview.filter_func = self.filter_match

        # Get the default layout manager based on the user's configuration.
        self.__preferred_layout_manager_var = tk.StringVar()
        current_default_layout = pref.get_option("default_layout_manager")
        if not current_default_layout:
            self.__preferred_layout_manager_var.set("pack")
        else:
            self.__preferred_layout_manager_var.set(current_default_layout)

        # Set the default layout manager
        self.default_layout_manager = self.__preferred_layout_manager_var.get()

        # Get whether we should center the toplevel preview window
        self.center_preview = pref.get_option("center_preview")

        # Filter vars
        self.filter_on = False
        self.filtervar = app.builder.get_variable("filtervar")
        self.filter_btn = app.builder.get_object("filterclear_btn")
        self.filter_prev_value = ""
        self.filter_prev_sitem = None
        self._detached = []
        self._listen_object_updates = True

        self.config_treeview()
        self.config_filter()

        # current item being edited
        self.current_edit = None

        # set global validator for tkvariables names
        TkVarPropertyEditor.global_validator = self.is_tkvar_valid
        # set global validator for IDs
        IdentifierPropertyEditor.global_validator = self.is_id_unique
        NamedIDPropertyEditor.global_validator = self.is_id_unique
        # set global validator for commands
        CommandPropertyBase.global_validator = self.is_command_valid
        # set global validator for bindings commands
        EventHandlerEditor.global_validator = self.is_binding_valid
        # set global validator for form field name entry
        FormFieldNameEntry.global_validator = self.is_form_fieldname_valid

        # Widget Editor
        pframe = app.builder.get_object("propertiesframe")
        # lframe = app.builder.get_object("layoutframe")
        lframe = app.builder.get_object("layouteditor1")
        bframe = app.builder.get_object("bindingsframe")
        bindingstree = app.builder.get_object("bindingstree")
        self.properties_editor = PropertiesEditor(
            pframe,
            reselect_item_func=partial(self.on_treeview_select, None),
        )
        # self.layout_editor = LayoutEditor(lframe)
        self.layout_editor = lframe
        self.bindings_editor = BindingsEditor(bindingstree, bframe)
        self.treeview.bind_all(
            "<<PreviewItemSelected>>", self._on_preview_item_clicked
        )

        def f(e, manager="grid"):
            self.change_container_manager(manager)

        lframe.bind_all("<<LayoutEditorContainerManagerToGrid>>", f)

        def f(e, manager="pack"):
            self.change_container_manager(manager)

        lframe.bind_all("<<LayoutEditorContainerManagerToPack>>", f)
        lframe.bind_all(
            "<<ClearSelectedGridTreeInfo>>",
            self.clear_selected_grid_tree_info,
        )
        lframe.bind_all(
            "<<NamedIDPropertyEditor::ResetID>>", self._on_reset_id_requested
        )

        # Tree Editing
        tree = self.treeview
        tree.bind_all(action.TREE_ITEM_COPY, lambda e: self.copy_to_clipboard())
        tree.bind_all(
            action.TREE_ITEM_PASTE, lambda e: self.paste_from_clipboard()
        )
        tree.bind_all(action.TREE_ITEM_CUT, lambda e: self.cut_to_clipboard())
        tree.bind_all(action.TREE_ITEM_DELETE, self.on_tree_item_delete)
        tree.bind_all(action.TREE_ITEM_DUPLICATE, self.on_tree_item_duplicate)
        tree.bind_all(
            action.TREE_ITEM_GRID_DOWN,
            lambda e: self.on_item_grid_move(self.GRID_DOWN),
        )
        tree.bind_all(
            action.TREE_ITEM_GRID_LEFT,
            lambda e: self.on_item_grid_move(self.GRID_LEFT),
        )
        tree.bind_all(
            action.TREE_ITEM_GRID_RIGHT,
            lambda e: self.on_item_grid_move(self.GRID_RIGHT),
        )
        tree.bind_all(
            action.TREE_ITEM_GRID_UP,
            lambda e: self.on_item_grid_move(self.GRID_UP),
        )
        tree.bind_all(action.TREE_ITEM_MOVE_UP, self.on_item_move_up)
        tree.bind_all(action.TREE_ITEM_MOVE_DOWN, self.on_item_move_down)
        tree.bind_all(action.TREE_NAV_UP, self.on_item_nav_up)
        tree.bind_all(action.TREE_NAV_DOWN, self.on_item_nav_down)
        tree.bind_all(
            action.TREE_ITEM_PREVIEW_TOPLEVEL, self.on_preview_in_toplevel
        )

        self.task_executor.start_processing()

    def _on_tree_configure(self, event):
        self.task_executor.add(self._stretch_main_column)

    def _stretch_main_column(self):
        w = self.treeview.winfo_width()
        stretch_col = "#0"
        stretch_col_cwidth = 0
        cols = [stretch_col]
        cols.extend(self.treeview.cget("displaycolumns"))
        csum = 0
        for col in cols:
            cwidth = self.treeview.column(col, "width")
            if col == stretch_col:
                stretch_col_cwidth = cwidth
            csum += cwidth
        space_left = w - csum - 4
        if space_left > 0:
            stretch_col_cwidth += space_left
            self.treeview.column(stretch_col, width=stretch_col_cwidth)
        self._stretch_cb = None

    def filter_match(self, tree, itemid, filter_value):
        txt = tree.item(itemid, "text").lower()
        match_found = filter_value in txt
        if not match_found:
            class_txt = self.treedata[itemid].classname.lower()
            match_found = filter_value in class_txt
        return match_found

    def on_tree_item_delete(self, event):
        selection = self.treeview.selection()
        if selection:
            do_delete = messagebox.askokcancel(
                _("Delete items"),
                _("Delete selected items?"),
                parent=self.treeview.winfo_toplevel(),
            )

            if do_delete:
                self.on_treeview_delete_selection(None)

    def clear_selected_grid_tree_info(self, event):
        """
        Clear the row/column text in the object treeview
        for the selected item.

        This gets called when the geometry manager of the
        currently selected widget changes from grid to pack or to place.

        This does not get used when multiple widgets need to have
        their geometry managers changed inside a container widget.
        """
        if self.current_edit:
            values = self.treeview.item(self.current_edit, "values")
            values = (values[0], "", "")
            self.treeview.item(self.current_edit, values=values)

    def selection_different_parents(self):
        """
        Check whether any of the selections have different parents.

        Return True if at least one selected item has a different parent than the rest of the selected items.

        The purpose of this method is: duplicating an item that has a different parent than the rest of the items
        will give the user unexpected results.

        For example:
        -> Frame1:
            -> Button1
            -> Frame2
               -> Button2

        In the example above, if the user attempts to duplicate Frame1 and Frame2 together, then Frame1 and Frame2 will get
        duplicated into root (because Frame1's parent is root). This may confuse the user.
        If we were to allow this, the end-result would show up like this:
        -> Frame1:
            -> Button1
            -> Frame2
               -> Button2
        ---Duplicated below as---
        -> Frame3
            -> Button3
            -> Frame4
               -> Button4
        -> Frame5
            -> Button5

        We use this method to decide whether we should allow a duplication to occur or not.
        """

        # Get all the selected items in the object treeview.
        all_selections = self.treeview.selection()

        if not all_selections:
            return False

        # Keep a record of the selected items' parents.
        parent_iids = []

        # Check whether any of the selected items have a different parent or
        # not.
        for selected_item in all_selections:

            # Get the parent of the current item we are looping on
            item_parent = self.treeview.parent(selected_item)

            # If item's parents has not been recorded, record it now.
            if item_parent not in parent_iids:
                parent_iids.append(item_parent)

                # Do we now have more than 1 parent? Break out of the loop if
                # that's the case.
                if len(parent_iids) > 1:
                    item_parent_in_selection = True
                    break

        else:
            # There are no selected items that have different parents.
            item_parent_in_selection = False

        return item_parent_in_selection

    def on_tree_item_duplicate(self, event):
        """
        Make a copy of the selected item (copy into a variable, not the clipboard)
        and 'paste' it in the parent of the selected item.

        The clipboard does not get used when making duplicates, but the process is very similar.
        """

        # Is the 'Duplicate' menu disabled? Don't allow this method to run.
        # Without this check here, the user can use Ctrl+D on their keyboard
        # and run this method.
        if self.app.duplicate_menu_state != "normal":
            return

        # Get the iids of all the selections. We need this to get the parent
        # iid of the first selection.
        selected_iid = self.treeview.selection()

        if not selected_iid:
            return
        else:
            # Get the iid of the first selection so we can later find out its
            # parent's iid.
            selected_iid = selected_iid[0]

        # Set a flag to indicate to copy_to_clipboard() that we will not
        # be using the clipboard, but a variable instead.
        self.duplicating = True
        self.copy_to_clipboard()

        # Record the selected items' parent iid (because we're going to paste
        # the widget(s) into the parent)
        self.duplicate_parent_iid = self.treeview.parent(selected_iid)

        # Paste the virtually-copied widget (not with the clipboard) to the
        # parent.
        self.treeview.event_generate(action.TREE_ITEM_PASTE)

    def change_container_manager(self, new_manager):
        item = self.current_edit
        parent = self.treeview.parent(item)
        gridrow = 0
        if parent:
            children = self.treeview.get_children(parent)
            # Stop listening object updates
            self._listen_object_updates = False

            # Update container manager info for parent
            self.treedata[parent].container_manager = new_manager

            # Update children
            for child in children:
                widget = self.treedata[child]
                # Don't change widgets with place manager
                # unless the selected widget's manager is being changed.
                if widget.manager != "place" or child == item:
                    widget.manager = new_manager  # Change manager

                    # update Tree R/C columns
                    values = self.treeview.item(child, "values")
                    if new_manager == "grid":
                        widget.layout_property("row", str(gridrow))
                        widget.layout_property("column", "0")
                        values = (values[0], gridrow, 0)
                        gridrow += 1
                    else:
                        values = (values[0], "", "")
                    self.treeview.item(child, values=values)
            self._listen_object_updates = True
            self.editor_edit(item, self.treedata[item])
            self.draw_widget(item)
            self.app.set_changed()

    def _on_preview_item_clicked(self, event):
        wid = self.previewer.selected_widget
        logger.debug("item-selected %s", wid)
        self.select_by_id(wid)

    def get_children_manager(self, parent, current_item=None):
        """Get layout manager for children of item"""
        manager = None
        children = self.treeview.get_children(parent)
        for child in children:
            child_manager = self.treedata[child].manager
            if child != current_item and child_manager != "place":
                manager = child_manager
                break
        return manager

    def get_container_info(self, item):
        """Return children count and grid dimension if container manager
        is grid."""
        children = self.treeview.get_children(item)
        count = len(children)
        grid_dim = None
        manager = self.get_children_manager(item)
        max_row = 0
        max_col = 0
        if manager == "grid":
            for item in children:
                wmeta = self.treedata[item]
                row = int(wmeta.layout_property("row"))
                if row > max_row:
                    max_row = row
                col = int(wmeta.layout_property("column"))
                if col > max_col:
                    max_col = col
            grid_dim = (max_row + 1, max_col + 1)

        cinfo = {
            "manager": manager,
            "has_children": bool(count),
            "grid_dim": grid_dim,
        }
        return cinfo

    def editor_edit(self, item, wdescr):
        self.current_edit = item
        manager_options = ["grid", "pack", "place"]
        parent_classname = None

        # Determine allowed manager options
        parent = self.treeview.parent(item)
        if parent:
            cm = self.get_children_manager(parent, item)
            if "grid" == cm:
                manager_options.remove("pack")
            if "pack" == cm:
                manager_options.remove("grid")
            parent_classname = self.get_widget_class(parent)
        logger.debug(manager_options)

        # Prepare container layout options
        cinfo = self.get_container_info(item)
        cmanager = cinfo["manager"]
        if cmanager is None:
            # Allow simple propagate option.
            wdescr.container_manager = "pack"
        elif cmanager != wdescr.container_manager:
            # Update widged description
            wdescr.container_manager = cmanager

        # Prepare field name values
        FormFieldNameSelector.FIELD_NAMES = self.get_form_fieldname_list()

        self.properties_editor.edit(wdescr)
        self.layout_editor.edit(
            wdescr, manager_options, cinfo, parent_classname
        )
        self.bindings_editor.edit(wdescr)
        self.get_form_fieldname_list()

    def editor_hide_all(self):
        self.properties_editor.hide_all()
        self.layout_editor.hide_all()
        self.bindings_editor.hide_all()

    def config_filter(self):
        def on_filtervar_changed(varname, element, mode):
            self.treeview.filter_by(self.filtervar.get())

        self.filtervar.trace_add("write", on_filtervar_changed)

        def on_filterbtn_click():
            self.filtervar.set("")

        self.filter_btn.configure(command=on_filterbtn_click)

    def config_treeview(self):
        """Sets treeview columns and other params"""
        tree = self.treeview
        tree.bind("<Double-1>", self.on_treeview_double_click)
        tree.bind("<<TreeviewSelect>>", self.on_treeview_select, add="+")

    def get_toplevel_parent(self, treeitem):
        """Returns the top level parent for treeitem."""
        tv = self.treeview
        toplevel_items = tv.get_children()

        item = treeitem
        while not (item in toplevel_items):
            item = tv.parent(item)

        return item

    def draw_widget(self, item):
        """Create a preview of the selected treeview item"""

        if item:
            self.treeview.filter_remove(remember=True)

            selected_id = self.treedata[item].identifier
            item = self.get_toplevel_parent(item)
            widget_id = self.treedata[item].identifier
            wclass = self.treedata[item].classname
            uidef = self.tree_to_uidef(item)
            self.previewer.draw(item, widget_id, uidef, wclass)
            self.previewer.show_selected(item, selected_id)
            self.treeview.filter_restore()

    def on_preview_in_toplevel(self, event=None):
        tv = self.treeview
        sel = tv.selection()
        if sel:
            self.treeview.filter_remove(remember=True)
            item = sel[0]
            item = self.get_toplevel_parent(item)
            widget_id = self.treedata[item].identifier
            uidef = self.tree_to_uidef(item)
            self.previewer.preview_in_toplevel(item, widget_id, uidef)
            self.treeview.filter_restore()
        else:
            logger.warning(_("No item selected."))

    def on_treeview_double_click(self, event=None):
        tv = self.treeview
        sel = tv.selection()
        # toplevel_items = tv.get_children()
        if sel:
            item = sel[0]
            if tv.parent(item) == "":
                # only redraw if toplevel is double clicked
                self.draw_widget(item)

    def on_treeview_delete_selection(self, event=None):
        """Removes selected items from treeview"""

        tv = self.treeview
        selection = tv.selection()

        # Need to remove filter
        self.treeview.filter_remove(remember=True)

        toplevel_items = tv.get_children()
        parents_to_redraw = set()
        final_focus = None
        for item in selection:
            try:
                parent = ""
                if item not in toplevel_items:
                    parent = self.get_toplevel_parent(item)
                else:
                    self.previewer.delete(item)
                # determine final focus
                if final_focus is None:
                    candidates = (
                        tv.prev(item),
                        tv.next(item),
                        tv.parent(item),
                    )
                    for c in candidates:
                        if c and (c not in selection):
                            final_focus = c
                            break
                # remove item and all its descendants
                self.delete_item_data(item)
                tv.delete(item)
                self.app.set_changed()
                if parent and (parent not in selection):
                    parents_to_redraw.add(parent)
                self.editor_hide_all()
            except tk.TclError:
                # Selection of parent and child items ??
                # TODO: notify something here
                pass
        # redraw widgets
        for item in parents_to_redraw:
            self.draw_widget(item)
        # Set final item focused
        if final_focus:
            selected_id = self.treedata[final_focus].identifier
            self.task_executor.add(lambda: tv.selection_set(final_focus))
            self.task_executor.add(lambda: tv.focus(final_focus))
            self.task_executor.add(lambda: tv.see(final_focus))
            self.task_executor.add(
                lambda i=final_focus, s=selected_id: self.previewer.show_selected(
                    i, s
                )
            )

        # No widget/item is currently selected anymore because
        # we've just deleted selected items from the treeview.
        self.current_edit = None

        # restore filter
        self.treeview.filter_restore()

    def delete_item_data(self, item):
        """
        Delete the item and all its descendants from self.treedata

        Arguments:

        - item: the item iid (str) to delete, such as 'I001'
        """

        # Get the children of the item.
        item_children = self.treeview.get_children(item)

        for child in item_children:
            self.delete_item_data(child)

        del self.treedata[item]

    def new_uidefinition(self):
        author = f"PygubuDesigner {pygubudesigner.__version__}"
        uidef = UIDefinition(wmetaclass=WidgetMeta, author=author)
        return uidef

    def tree_to_uidef(self, treeitem=None):
        """Traverses treeview and generates a ElementTree object"""

        # Need to remove filter or hidden items will not be saved.
        self.treeview.filter_remove(remember=True)

        uidef = self.new_uidefinition()
        if treeitem is None:
            items = self.treeview.get_children()
            for item in items:
                node = self.build_uidefinition(uidef, "", item)
                uidef.add_xmlnode(node)
        else:
            node = self.build_uidefinition(uidef, "", treeitem)
            uidef.add_xmlnode(node)

        # restore filter
        self.treeview.filter_restore()

        return uidef

    def build_uidefinition(self, uidef, parent, item):
        """Traverses tree and build ui definition"""

        node = uidef.widget_to_xmlnode(self.treedata[item])

        children = self.treeview.get_children(item)
        for child in children:
            child_node = self.build_uidefinition(uidef, item, child)
            uidef.add_xmlchild(node, child_node)
        return node

    def _treeitem_label(self, data):
        identifier = f"{data.identifier}: " if data.is_named else " "
        treelabel = f"{identifier}{data.classname.split('.')[-1]}"
        return treelabel

    def _insert_item(
        self, root, data, from_file=False, is_first_widget_pasted=False
    ):
        """Insert a item on the treeview and fills columns from data

        The argument: is_first_widget_pasted (bool) will be True if we're about to
        insert the first widget that was pasted from the clipboard or duplicated.
        Here 'first widget' is basically the 'outer widget' - the widget whose direct
        parent is the container that it was pasted in.

        If we're currently on an outer widget (is_first_widget_pasted=True) that was
        pasted or duplicated, we need to see if any of its siblings have the same
        row AND column, and if they do, we need to give the pasted widget a new unique
        row number so it doesn't overlap with its new siblings.

        If we're not currently dealing with an outer widget, that means it's a child of
        the outer widget and we should not change the row/columns of the outer widget's
        children widgets.
        """

        data.setup_defaults()  # load default settings for properties and layout
        tree = self.treeview
        treelabel = self._treeitem_label(data)
        row = col = ""
        if root != "" and data.has_layout_defined():
            if data.manager == "grid" and data.layout_required:
                row = data.layout_property("row")
                col = data.layout_property("column")
                # Fix grid row position when using copy and paste
                if not from_file:
                    if is_first_widget_pasted:
                        # Increase the pasted widget by 1 row (if necessary)
                        # so that it doesn't overlap
                        row = self.get_available_row(root, data)

                    data.layout_property("row", row)

        image = ""
        try:
            image = StockImage.get("16x16-tk.default")
        except StockImageException:
            # TODO: notify something here
            pass

        try:
            image = StockImage.get(f"16x16-{data.classname}")
        except StockImageException:
            # TODO: notify something here
            pass

        values = (data.classname, row, col)
        item = tree.insert(
            root, "end", text=treelabel, values=values, image=image
        )
        data.attach(self)
        self.treedata[item] = data

        self.app.set_changed()

        return item

    def copy_to_clipboard(self):
        """
        Copies selected items to clipboard.
        """
        tree = self.treeview
        # get the selected item:
        selection = tree.selection()
        logger.debug("Selection %s", selection)
        if selection:
            self.treeview.filter_remove(remember=True)

            uidef = self.new_uidefinition()
            for item in selection:
                node = self.build_uidefinition(uidef, "", item)
                uidef.add_xmlnode(node)
            text = str(uidef)

            if self.duplicating:
                self.virtual_clipboard_for_duplicate = text
            else:
                tree.clipboard_clear()
                tree.clipboard_append(text)

            self.treeview.filter_restore()

    def cut_to_clipboard(self):
        self.copy_to_clipboard()
        self.on_treeview_delete_selection()

    def _validate_add(self, root_item, classname, show_warnings=True):
        is_valid = True

        new_boclass = CLASS_MAP[classname].builder
        root = root_item
        if root:
            root_classname = self.treedata[root].classname
            root_boclass = CLASS_MAP[root_classname].builder
            allowed_children = root_boclass.allowed_children
            allowed_children = (
                [] if allowed_children is None else allowed_children
            )
            canbe_parent = root_boclass.canbe_parent_of(new_boclass, classname)
            if not canbe_parent:
                if show_warnings:
                    str_children = ", ".join(allowed_children)
                    msg = _("Allowed children: %s.")
                    logger.warning(msg, str_children)
                is_valid = False
                return is_valid

            children_count = len(self.treeview.get_children(root))
            maxchildren = root_boclass.maxchildren
            if maxchildren is not None and children_count >= maxchildren:
                if show_warnings:
                    msg = trlog(
                        _("Only {0} children allowed for {1}"),
                        maxchildren,
                        root_classname,
                    )
                    logger.warning(msg)
                is_valid = False
                return is_valid

            # allowed_parents = new_boclass.allowed_parents
            # if (
            #    allowed_parents is not None
            #    and root_classname not in allowed_parents
            # ):
            if not new_boclass.canbe_child_of(root_boclass, root_classname):
                if show_warnings:
                    msg = trlog(
                        _("{0} not allowed as parent of {1}"),
                        root_classname,
                        classname,
                    )
                    logger.warning(msg)
                is_valid = False
                return is_valid

            if not canbe_parent and root_boclass.container is False:
                if show_warnings:
                    msg = _("Not allowed, %s is not a container.")
                    logger.warning(msg, root_classname)
                is_valid = False
                return is_valid

        else:
            # allways show warning when inserting in top level
            # if insertion is at top level,
            # Validate if it can be added at root level
            allowed_parents = new_boclass.allowed_parents
            if allowed_parents is not None and "root" not in allowed_parents:
                if show_warnings:
                    msg = _("%s not allowed at root level")
                    logger.warning(msg, classname)
                is_valid = False
                return is_valid

            # if parents are not specified as parent,
            # check that item to insert is a container.
            # only containers are allowed at root level
            if new_boclass.container is False:
                if show_warnings:
                    msg = _("Not allowed at root level, %s is not a container.")
                    logger.warning(msg, classname)
                is_valid = False
                return is_valid
        return is_valid

    def _generate_id(self, classname, index):
        name = classname.split(".")[-1]

        if pref.get_option("widget_naming_separator") == "UNDERSCORE":
            name = f"{name}_{index}"
        else:
            name = f"{name}{index}"

        name = name.lower()

        if pref.get_option("widget_naming_ufletter") == "yes":
            name = name.capitalize()
        return name

    def get_unique_id(self, classname, start_id=None):
        if start_id is None:
            self.counter[classname] += 1
            start_id = self._generate_id(classname, self.counter[classname])

        is_defined = self._is_id_defined("", start_id)
        while is_defined is True:
            self.counter[classname] += 1
            start_id = self._generate_id(classname, self.counter[classname])
            is_defined = self._is_id_defined("", start_id)

        return start_id

    def paste_from_clipboard(self):
        self.treeview.filter_remove(remember=True)

        tree = self.treeview
        selected_item = ""

        if self.duplicating:
            # Simulate the selected item (the one we're pasting to) as the
            # parent of the first selected item we're duplicating.
            selected_item = self.duplicate_parent_iid
        else:
            selection = tree.selection()
            if selection:
                selected_item = selection[0]
        try:
            # If we're duplicating, we should get the copy data from a
            # variable, not the clipboard.
            if self.duplicating:
                # Get the copy/duplicate data.
                text = self.virtual_clipboard_for_duplicate
            else:
                text = tree.selection_get(selection="CLIPBOARD")

            uidef = self.new_uidefinition()
            uidef.load_from_string(text)
            for wmeta in uidef.widgets():
                if self._validate_add(selected_item, wmeta.classname):
                    self.update_layout(selected_item, wmeta)
                    self.populate_tree(
                        selected_item,
                        uidef,
                        wmeta,
                        is_first_widget_pasted=True,
                    )
        except ET.ParseError:
            msg = "The clipboard does not have a valid widget xml definition."
            logger.error(msg)
        except tk.TclError:
            pass
        finally:
            self.duplicating = False
            self.virtual_clipboard_for_duplicate = None

        if selected_item == "":
            # redraw all
            children = tree.get_children("")
            for child in children:
                self.draw_widget(child)
        else:
            self.draw_widget(selected_item)

        self.treeview.filter_restore()

        # Get all the children widgets of the parent that we pasted into.
        children_of_parent = self.treeview.get_children(selected_item)
        if children_of_parent:
            # Select the last (latest) child so the user can see where the last
            # pasted item is.
            self.task_executor.add(
                lambda: self.treeview.selection_set(children_of_parent[-1])
            )
            self.task_executor.add(
                lambda: self.treeview.focus(children_of_parent[-1])
            )
            self.task_executor.add(
                lambda: self.treeview.see(children_of_parent[-1])
            )

    def update_layout(self, root, data):
        """Removes layout info from element, when copied from clipboard."""

        cmanager = self.get_children_manager(root)
        cmanager = (
            cmanager if cmanager is not None else self.default_layout_manager
        )
        emanager = data.manager
        if emanager != "place" and cmanager != emanager:
            data.manager = cmanager

    def add_widget(self, wclass):
        """Adds a new item to the treeview."""

        tree = self.treeview
        #  get the selected item:
        selected_item = ""
        tsel = tree.selection()
        if tsel:
            selected_item = tsel[0]

        #  Need to remove filter if set
        self.treeview.filter_remove()

        root = selected_item
        #  check if the widget can be added at selected point
        parent = tree.parent(root)
        has_parent = parent != root
        show_warnings = False if has_parent else True
        if not self._validate_add(root, wclass, show_warnings):
            #  if not try to add at item parent level
            parent = tree.parent(root)
            if parent != root:
                logger.info("Failed to add widget, trying one level up.")
                if self._validate_add(parent, wclass):
                    root = parent
                else:
                    return
            else:
                return

        #  root item should be set at this point
        #  setup properties
        parent = None
        if root:
            parent = self.treedata[root]
        manager = self.default_layout_manager  # << DEFAULT LAYOUT MANAGER
        if parent is not None:
            cmanager = self.get_children_manager(root)
            manager = cmanager if cmanager else manager

        widget_id = self.get_unique_id(wclass)
        pdefaults, ldefaults = WidgetMeta.get_widget_defaults(wclass, widget_id)
        data = WidgetMeta(wclass, widget_id, manager, pdefaults, ldefaults)
        data.is_named = False
        data.identifier = widget_id

        # Recalculate position if manager is grid
        if manager == "grid":
            rownum = "0"
            if root:
                rownum = str(self.get_max_row(root) + 1)
            data.layout_property("row", rownum)
            data.layout_property("column", "0")

        item = self._insert_item(root, data)

        # Do redraw
        self.draw_widget(item)

        # Select and show the item created
        # tree.after_idle(lambda: tree.selection_set(item))
        # tree.after_idle(lambda: tree.focus(item))
        # tree.after_idle(lambda: tree.see(item))
        self.task_executor.add(lambda: tree.selection_set(item))
        self.task_executor.add(lambda: tree.focus(item))
        self.task_executor.add(lambda: tree.see(item))

    def remove_all(self):
        self.treedata = {}
        self.treeview.filter_remove()
        children = self.treeview.get_children()
        if children:
            self.treeview.delete(*children)
        self.editor_hide_all()
        self.counter.clear()  # Reset the widget counter (August 19, 2021)
        self.current_edit = (
            None  # We no longer have a selected item in the treeview
        )

    def load_file(self, project: Project):
        """Load file into treeview"""

        self.counter.clear()
        self.remove_all()
        self.previewer.remove_all()
        self.editor_hide_all()

        dirname = project.fpath.parent
        self.previewer.resource_paths.append(dirname)
        uidef = project.uidefinition
        for widget in uidef.widgets():
            self.populate_tree("", uidef, widget, from_file=True)

        children = self.treeview.get_children("")
        for child in children:
            self.draw_widget(child)
        self.previewer.show_selected(None, None)

    def populate_tree(
        self,
        master,
        uidef,
        wmeta,
        from_file=False,
        is_first_widget_pasted=False,
    ):
        """Reads xml nodes and populates tree item

        The argument: is_first_widget_pasted (bool) will be True if we're currently
        on the first widget that was pasted from the clipboard or duplicated.
        """

        cname = wmeta.classname
        original_id = wmeta.identifier
        uniqueid = self.get_unique_id(cname, wmeta.identifier)
        wmeta.widget_property("id", uniqueid)

        if cname in CLASS_MAP:

            pwidget = self._insert_item(
                master,
                wmeta,
                from_file=from_file,
                is_first_widget_pasted=is_first_widget_pasted,
            )

            for mchild in uidef.widget_children(original_id):
                self.populate_tree(pwidget, uidef, mchild, from_file=from_file)
        else:
            raise Exception(f'Class "{cname}" not mapped')

    def get_available_row(self, parent, new_item_data):
        """
        Determine if new_item's row and column conflict with
        its new siblings (the children of parent).

        If the row AND column of one the siblings matches the new item's row/col,
        set new_item's row to be the maximum row of all its siblings + 1.

        The purpose of this method is to avoid new_item from getting overlapped with any
        of its sibling and to also avoid unnecessarily increasing the row number of new_item
        if it's not necessary (for example: new_item may not have any siblings with the same row/col,
        so in a case like that, there is no point in changing new_item's row number).

        This method is only used when widget(s) are being pasted/duplicated.

        Arguments:

        - parent (str): the parent's item iid (ie: I001). This will be the parent
        that the new item was pasted into or duplicated into.

        - new_item_data (str): the wmeta data for the item that is being pasted.
        """

        increase_row = False
        max_row = 0

        # Get the row/col for the item being pasted
        new_item_row = new_item_data.layout_property("row")
        new_item_column = new_item_data.layout_property("column")
        new_item_name = new_item_data.identifier

        # Check new_item's siblings to see if any of them have the exact same row/col.
        children = self.treeview.get_children(parent)
        for sibling in children:

            sibling_properties = self.treedata[sibling]
            sibling_name = sibling_properties.identifier

            # Don't check new_item because we're checking its siblings, not itself.
            if sibling_name != new_item_name:

                # Get the row/col of the new item's sibling.
                sibling_row = sibling_properties.layout_property("row")
                sibling_col = sibling_properties.layout_property("column")

                # Keep track of the max row number in the new item's column,
                # because we may need to use it after the loop is done.
                if (
                    sibling_col == new_item_column
                    and int(sibling_row) > max_row
                ):
                    max_row = int(sibling_row)

                # If the item that is being pasted (the new item) has the same
                # row AND column as one its new siblings, then we need to set
                # the new item's row number to max_rows + 1.
                if (
                    sibling_row == new_item_row
                    and sibling_col == new_item_column
                ):

                    # Set the flag but keep the loop going because we still
                    # need to find out what the max row number is.
                    increase_row = True

        if increase_row:
            new_item_row = str(max_row + 1)

        return new_item_row

    def get_max_row(self, item):
        tree = self.treeview
        max_row = -1
        children = tree.get_children(item)
        for child in children:
            row = self.treedata[child].layout_property("row")
            row = int(row)
            if row > max_row:
                max_row = row
        return max_row

    def on_treeview_select(self, event):
        tree = self.treeview
        sel = tree.selection()
        if sel:
            item = sel[0]
            top = self.get_toplevel_parent(item)
            selected_id = self.treedata[item].identifier
            self.previewer.show_selected(top, selected_id)
            # max_rc = self.get_max_row_col(item)
            self.editor_edit(item, self.treedata[item])
        else:
            # No selection hide all
            self.editor_hide_all()

        # Check if some menu items (such as 'Duplicate') should be disabled or not.
        # The reason is: the treeview selection has changed, so we need to evaluate
        # whether it makes sense to have some menus enabled or not.
        self.app.evaluate_menu_states()

    def on_user_request_redraw(self, event=None):
        tv = self.treeview
        sel = tv.selection()
        # toplevel_items = tv.get_children()
        if sel:
            item = sel[0]
            top_item = self.get_toplevel_parent(item)
            self.draw_widget(top_item)

    def update_tree_data_display(self, item, data):
        """Updates tree colums when itemdata is changed."""
        tree = self.treeview
        item_text = self._treeitem_label(data)
        if item_text != tree.item(item, "text"):
            tree.item(item, text=item_text)
        # if tree.parent(item) != '' and 'layout' in data:
        if tree.parent(item) != "" and data.layout_required:
            if data.manager == "grid":
                row = data.layout_property("row")
                col = data.layout_property("column")
                values = tree.item(item, "values")
                if row != values[1] or col != values[2]:
                    values = (data.classname, row, col)
                tree.item(item, values=values)

    def preview_widget_update(self, item, hint, data):
        """Update widget preview.
        If posible, it will update widget properties live.
        Otherwise, a full widget redraw is done.
        """

        full_redraw = (hint & WidgetMeta.PROPERTY_RO_CHANGED) | (
            hint & WidgetMeta.LAYOUT_MANAGER_CHANGED
        )

        if full_redraw:
            # Needs full redraw.
            self.draw_widget(item)
            return

        preview_id = self.get_toplevel_parent(item)
        if (
            hint & WidgetMeta.PROPERTY_DATA_CHANGED
            and hint & WidgetMeta.PROPERTY_ID_CHANGED
        ):
            old_id = data.old_data["id"]
            new_id = data.identifier
            self.previewer.rename_preview_widget(preview_id, old_id, new_id)
            return

        if self.update_builder is None:
            self.update_builder = Builder()

        # Maybe just needs update.
        widget_id = data.identifier
        bclass = data.classname
        widget = self.previewer.preview_for_widget(preview_id, widget_id)
        if bclass not in self.update_bo:
            bo_class = PluginManager.get_preview_builder_for(bclass)
            bo_class = (
                CLASS_MAP[bclass].builder if bo_class is None else bo_class
            )
            self.update_bo[bclass] = bo_class(self.update_builder, data)
        wbuilder = self.update_bo[bclass]
        # Use copy here because preview builders can change data for preview
        meta_copy = WidgetMeta(bclass, widget_id)
        meta_copy.copy_properties(data)
        wbuilder.wmeta = meta_copy
        wbuilder.widget = widget

        property_was_blanked = hint & WidgetMeta.PROPERTY_BLANKED

        if hint & WidgetMeta.PROPERTY_CHANGED:
            wbuilder.configure()
            if property_was_blanked:
                wbuilder.unset_property(data.prop_blanked)
        if hint & WidgetMeta.LAYOUT_PROPERTY_CHANGED:
            reset_layout = property_was_blanked
            wbuilder.layout(forget=reset_layout)

            # FIXME: When propagate property is changed
            # calculations are not correct unless a property
            # is reconfigured ?
            wbuilder.configure()
        if hint & WidgetMeta.BINDING_CHANGED:
            # Do nothing now
            pass
        self.previewer.update_preview_bbox(preview_id)
        self.previewer.show_selected(preview_id, widget_id)

    def update_event(self, hint, data):
        """Manages notify event when data is changed."""

        if not self._listen_object_updates:
            return

        item = self.get_item_by_data(data)
        if item:
            self.update_tree_data_display(item, data)
            self.preview_widget_update(item, hint, data)
            self.app.set_changed()

    def schedule_preview_update(self, item):
        """Schedule a preview update.
        Helps to reduce full redraw when moving widget in treeview with keyboard.
        """
        if item not in self.scheduled_widget_updates:
            self.scheduled_widget_updates.append(item)
        if self.preview_update_cbid is not None:
            self.treeview.after_cancel(self.preview_update_cbid)
        self.preview_update_cbid = self.treeview.after(
            950, self.schedule_preview_update_execute
        )

    def schedule_preview_update_execute(self):
        for item in self.scheduled_widget_updates:
            self.draw_widget(item)
        self.scheduled_widget_updates.clear()
        self.preview_update_cbid = None

    def get_item_by_data(self, data):
        skey = None
        for key, value in self.treedata.items():
            if value == data:
                skey = key
                break
        return skey

    def on_item_nav_up(self, event=None):
        """Move selection to prev item"""
        tree = self.treeview
        sel = tree.selection()
        if sel:
            item = sel[0]
            prev = tree.prev(item)
            if prev and tree.item(prev, "open"):
                children = tree.get_children(prev)
                if children:
                    prev = children[-1]
            if not prev:
                prev = tree.parent(item)
            if prev:
                tree.selection_set(prev)

    def on_item_nav_down(self, event=None):
        """Move selection to next item"""
        tree = self.treeview
        sel = tree.selection()
        if sel:
            item = sel[0]
            next_ = None
            if tree.item(item, "open"):
                # children
                children = tree.get_children(item)
                if children:
                    next_ = children[0]
            if not next_:
                # sibling
                next_ = tree.next(item)
            if not next_:
                # parent sibling
                parent = tree.parent(item)
                next_ = tree.next(parent)
            if next_:
                tree.selection_set(next_)

    def on_item_move_up(self, event):
        tree = self.treeview
        sel = tree.selection()
        if sel:
            self.treeview.filter_remove(remember=True)
            item = sel[0]
            parent = tree.parent(item)
            prev = tree.prev(item)
            if prev:
                prev_idx = tree.index(prev)
                tree.move(item, parent, prev_idx)
                item_data = self.treedata[item]
                manager = item_data.manager
                layout_required = item_data.layout_required
                self.app.set_changed()

                # Always refresh preview for objects that don't
                # require a layout, such as menus and notebook tabs.
                if manager in ("pack", "place") or not layout_required:
                    # self.draw_widget(item)
                    self.schedule_preview_update(item)
            self.treeview.filter_restore()

    def on_item_move_down(self, event):
        tree = self.treeview
        sel = tree.selection()
        if sel:
            self.treeview.filter_remove(remember=True)
            item = sel[0]
            parent = tree.parent(item)
            next = tree.next(item)
            if next:
                next_idx = tree.index(next)
                tree.move(item, parent, next_idx)
                item_data = self.treedata[item]
                manager = item_data.manager
                layout_required = item_data.layout_required
                self.app.set_changed()

                # Always refresh preview for objects that don't
                # require a layout, such as menus and notebook tabs.
                if manager in ("pack", "place") or not layout_required:
                    # self.draw_widget(item)
                    self.schedule_preview_update(item)
            self.treeview.filter_restore()

    #
    # Item grid move functions
    #
    def on_item_grid_move(self, direction):
        tree = self.treeview
        selection = tree.selection()
        if selection:
            self.treeview.filter_remove(remember=True)
            for item in selection:
                data = self.treedata[item]

                if data.manager != "grid":
                    break

                current_row = new_row = int(data.layout_property("row"))
                current_col = new_col = int(data.layout_property("column"))
                if direction == self.GRID_UP:
                    if current_row > 0:
                        new_row = current_row - 1
                elif direction == self.GRID_DOWN:
                    new_row = current_row + 1
                elif direction == self.GRID_LEFT:
                    if current_col > 0:
                        new_col = current_col - 1
                elif direction == self.GRID_RIGHT:
                    new_col = current_col + 1

                if current_row != new_row:
                    data.layout_property("row", str(new_row))
                    data.notify(WidgetMeta.LAYOUT_PROPERTY_CHANGED)
                if current_col != new_col:
                    data.layout_property("column", str(new_col))
                    data.notify(WidgetMeta.LAYOUT_PROPERTY_CHANGED)
            self.treeview.filter_restore()

    def _top_widget_iterator(self):
        children = self.treeview.get_children("")
        for item in children:
            data = self.treedata[item]
            yield (item, data)

    def _data_iterator(self, root=None):
        start = "" if root is None else root
        children = self.treeview.get_children(start)
        for item in children:
            data = self.treedata[item]
            yield (item, data)
        for item in children:
            yield from self._data_iterator(item)

    def get_tree_topitem_byid(self, wid):
        for item, data in self._top_widget_iterator():
            if data.identifier == wid:
                return item
        return None

    def get_top_widget_list(self):
        wlist = []
        for item, data in self._top_widget_iterator():
            if data.classname != "tk.Menu":
                label = f"{data.identifier} ({data.classname})"
                element = (item, label)
                wlist.append(element)
        return wlist

    def get_top_menu_list(self):
        wlist = []
        for item, data in self._top_widget_iterator():
            if data.classname == "tk.Menu":
                label = f"{data.identifier} ({data.classname})"
                element = (item, label)
                wlist.append(element)
        return wlist

    def get_options_for_project_settings(self):
        main_widget = OrderedDict()
        main_menu = OrderedDict()
        for item, data in self._top_widget_iterator():
            label = f"{data.identifier} ({data.classname})"
            if data.classname == "tk.Menu":
                main_menu[data.identifier] = label
            else:
                main_widget[data.identifier] = label
        return dict(main_widget=main_widget, main_menu=main_menu)

    def get_widget_class(self, item):
        return self.treedata[item].classname

    def get_widget_id(self, item):
        return self.treedata[item].identifier

    def select_by_id(self, widget_id):
        found = None
        for item, data in self.treedata.items():
            if widget_id == data.identifier:
                found = item
                break
        if found:
            tree = self.treeview
            self.treeview.filter_remove()
            self.treeview.expand_to(found)
            self.task_executor.add(lambda: tree.selection_set(found))
            self.task_executor.add(lambda: tree.focus(found))
            self.task_executor.add(lambda: tree.see(found))

    def is_id_unique(self, idvalue) -> bool:
        "Check if idvalue is unique in all UI tree."
        is_unique = (
            not self._is_id_defined("", idvalue)
            and not self._is_tkvar_defined("", idvalue)
            and not self._is_command_defined("", idvalue)
            and not self._is_binding_defined("", idvalue)
        )
        return is_unique

    def _is_id_defined(self, root, widget_id) -> bool:
        """Search widget id in the tree."""
        is_defined = False
        if root != "":
            data = self.treedata[root]
            if data.identifier == widget_id:
                is_defined = True
        if is_defined is False:
            for item in self.treeview.get_children(root):
                is_defined = self._is_id_defined(item, widget_id)
                if is_defined is True:
                    break
        return is_defined

    def _is_tkvar_defined(self, root, varname) -> bool:
        """Search variable name in the tree."""
        is_defined = False
        if root != "":
            data = self.treedata[root]
            builder = CLASS_MAP[data.classname].builder
            for pname, value in data.properties.items():
                if pname in builder.tkvar_properties:
                    vname = value
                    if ":" in value:
                        vtype, vname = value.split(":")
                    if vname == varname:
                        is_defined = True
        if is_defined is False:
            for item in self.treeview.get_children(root):
                is_defined = self._is_tkvar_defined(item, varname)
                if is_defined is True:
                    break
        return is_defined

    def _is_binding_defined(self, root, cbname) -> bool:
        """Search callback binding name in the tree."""
        is_defined = False
        if root != "":
            data = self.treedata[root]
            for bind in data.bindings:
                if bind.handler == cbname:
                    is_defined = True
        if is_defined is False:
            for item in self.treeview.get_children(root):
                is_defined = self._is_binding_defined(item, cbname)
                if is_defined is True:
                    break
        return is_defined

    def _is_command_defined(self, root, command_name) -> bool:
        """Searh command name in the tree."""
        is_defined = False
        if root != "":
            data = self.treedata[root]
            builder = CLASS_MAP[data.classname].builder
            for pname, value in data.properties.items():
                if pname in builder.command_properties:
                    cmd = json.loads(value)
                    if command_name == cmd["value"]:
                        is_defined = True
        if is_defined is False:
            for item in self.treeview.get_children(root):
                is_defined = self._is_command_defined(item, command_name)
                if is_defined is True:
                    break
        return is_defined

    def is_command_valid(self, cmdname):
        """Check if command name does not collide with other names."""
        is_valid = (
            not self._is_id_defined("", cmdname)
            and not self._is_binding_defined("", cmdname)
            and not self._is_tkvar_defined("", cmdname)
        )
        return is_valid

    def is_tkvar_valid(self, varname):
        """Check if tkvarname does not collide with other names."""
        is_valid = (
            not self._is_id_defined("", varname)
            and not self._is_command_defined("", varname)
            and not self._is_binding_defined("", varname)
        )
        return is_valid

    def is_binding_valid(self, cmdname):
        """Check if binding name does not collide with other names."""
        is_valid = (
            not self._is_id_defined("", cmdname)
            and not self._is_command_defined("", cmdname)
            and not self._is_tkvar_defined("", cmdname)
        )
        return is_valid

    def _on_reset_id_requested(self, event=None):
        item = self.current_edit
        wmeta = self.treedata[item]
        # Stop listening object updates
        self._listen_object_updates = False
        # Reset object identifier
        newid = self.get_unique_id(wmeta.classname)
        wmeta.start_id = None
        wmeta.start_named = None
        wmeta.identifier = newid
        wmeta.is_named = False

        self._listen_object_updates = True
        self.editor_edit(item, wmeta)
        self.draw_widget(item)
        self.app.set_changed()

    def _is_form_field_class(self, classname: str):
        builder = CLASS_MAP[classname].builder
        if builder.class_ is not None:
            return issubclass(builder.class_, FieldWidget)
        return False

    def _is_form_filedname_defined(self, fieldname: str):
        is_defined = False
        for item, data in self._data_iterator():
            if self._is_form_field_class(data.classname):
                fname = data.widget_property("field_name")
                if not fname:
                    fname = data.identifier
                if fname == fieldname:
                    is_defined = True
                    break
        return is_defined

    def get_form_fieldname_list(self):
        flist = []
        for item, data in self._data_iterator():
            if self._is_form_field_class(data.classname):
                fname = data.widget_property("field_name")
                if not fname:
                    fname = data.identifier
                flist.append(fname)
        return flist

    def is_form_fieldname_valid(self, fieldname: str):
        return not self._is_form_filedname_defined(fieldname)
