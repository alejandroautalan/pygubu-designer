# encoding: UTF-8
#
# Copyright 2012-2013 Alejandro Autalán
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

from __future__ import unicode_literals

import os
import xml.etree.ElementTree as ET
from collections import Counter
import logging
try:
    import tkinter as tk
    from tkinter import messagebox
except:
    import Tkinter as tk
    import tkMessageBox as messagebox

from pygubu.builder import CLASS_MAP
from pygubu.builder.uidefinition import UIDefinition
from pygubu.stockimage import StockImage, StockImageException
import pygubudesigner
from .widgetdescr import WidgetMeta
from .i18n import translator as _
from .util import trlog
from .propertieseditor import PropertiesEditor
from .bindingseditor import BindingsEditor
from .layouteditor import LayoutEditor
from .i18n import translator
from .actions import *
from pygubudesigner import preferences as pref


logger = logging.getLogger('pygubu.designer')

#translator function
_ = translator


class WidgetsTreeEditor(object):
    GRID_UP = 0
    GRID_DOWN = 1
    GRID_LEFT = 2
    GRID_RIGHT = 3

    def __init__(self, app):
        self.app = app
        self.treeview = app.treeview
        self.previewer = app.previewer
        self.treedata = {}
        self.counter = Counter()
        self.default_layout_manager = 'pack' # TODO: set from configuration
        # Filter vars
        self.filter_on = False
        self.filtervar = app.builder.get_variable('filtervar')
        self.filter_btn = app.builder.get_object('filterclear_btn')
        self.filter_prev_value = ''
        self.filter_prev_sitem = None
        self._detached = []
        self._listen_object_updates = True

        self.config_treeview()
        self.config_filter()
        
        # current item being edited
        self.current_edit = None

        # Widget Editor
        pframe = app.builder.get_object('propertiesframe')
        lframe = app.builder.get_object('layoutframe')
        bframe = app.builder.get_object('bindingsframe')
        bindingstree = app.builder.get_object('bindingstree')
        
        self.properties_editor = PropertiesEditor(
            pframe, id_validator=self.is_id_unique)
        self.layout_editor = LayoutEditor(lframe)
        self.bindings_editor = BindingsEditor(bindingstree, bframe)
        self.treeview.bind_all('<<PreviewItemSelected>>', self._on_preview_item_clicked)
        # Listen to Grid RC changes from layout
        lframe.bind_all('<<LayoutEditorGridRCChanged>>', self._on_gridrc_changed)
        f = lambda e, manager='grid': self.change_container_manager(manager)
        lframe.bind_all('<<LayoutEditorContainerManagerToGrid>>', f)
        f = lambda e, manager='pack': self.change_container_manager(manager)
        lframe.bind_all('<<LayoutEditorContainerManagerToPack>>', f)
        
        # Tree Editing
        tree = self.treeview
        tree.bind_all(TREE_ITEM_COPY, lambda e: self.copy_to_clipboard())
        tree.bind_all(TREE_ITEM_PASTE, lambda e: self.paste_from_clipboard())
        tree.bind_all(TREE_ITEM_CUT, lambda e: self.cut_to_clipboard())
        tree.bind_all(TREE_ITEM_DELETE, self.on_tree_item_delete)
        tree.bind_all(TREE_ITEM_GRID_DOWN,
                  lambda e: self.on_item_grid_move(self.GRID_DOWN))
        tree.bind_all(TREE_ITEM_GRID_LEFT,
                  lambda e: self.on_item_grid_move(self.GRID_LEFT))
        tree.bind_all(TREE_ITEM_GRID_RIGHT,
                  lambda e: self.on_item_grid_move(self.GRID_RIGHT))
        tree.bind_all(TREE_ITEM_GRID_UP,
                  lambda e: self.on_item_grid_move(self.GRID_UP))
        tree.bind_all(TREE_ITEM_MOVE_UP, self.on_item_move_up)
        tree.bind_all(TREE_ITEM_MOVE_DOWN, self.on_item_move_down)
        tree.bind_all(TREE_NAV_UP, self.on_item_nav_up)
        tree.bind_all(TREE_NAV_DOWN, self.on_item_nav_down)
        tree.bind_all(TREE_ITEM_PREVIEW_TOPLEVEL, self.on_preview_in_toplevel)
        
    def on_tree_item_delete(self, event):
        selection = self.treeview.selection()
        if selection:
            do_delete = messagebox.askokcancel(
                    _('Delete items'),
                    _('Delete selected items?'),
                    parent=self.treeview.winfo_toplevel())
            
            if do_delete:
                self.on_treeview_delete_selection(None)
    
    def _on_gridrc_changed(self, event):
        # update siblings items that have same row col position
        current_item = self.current_edit
        parent = self.treeview.parent(current_item)
        if parent:
            wmeta = self.treedata[current_item]
            srow = wmeta.layout_property('row')
            scol = wmeta.layout_property('column')
            children = self.treeview.get_children(parent)
            for child in children:
                if child == current_item:
                    continue
                wu = self.treedata[child]
                wu_row = wu.layout_property('row')
                wu_col = wu.layout_property('column')
                if wu_row == srow:
                    wu.copy_gridrc(wmeta, 'row')
                if wu_col == scol:
                    wu.copy_gridrc(wmeta, 'col')
    
    def change_container_manager(self, new_manager):
        item = self.current_edit
        parent = self.treeview.parent(item)
        gridrow = 0
        if parent:
            children = self.treeview.get_children(parent)
            # Stop listening object updates
            self._listen_object_updates = False

            for child in children:
                widget = self.treedata[child]
                widget.manager = new_manager  # Change manager
                
                #update Tree R/C columns
                values = self.treeview.item(child, 'values')
                if new_manager == 'grid':
                    widget.layout_property('row', str(gridrow))
                    widget.layout_property('column', '0')
                    values = (values[0], gridrow, 0)
                    gridrow += 1
                else:
                    values = (values[0], '', '')
                self.treeview.item(child, values=values)
            self._listen_object_updates = True
            self.editor_edit(item, self.treedata[item])
            self.draw_widget(item)
            self.app.set_changed()

    def _on_preview_item_clicked(self, event):
        wid = self.previewer.selected_widget
        logger.debug('item-selected %s', wid)
        self.select_by_id(wid)
        
    def get_children_manager(self, item, current=None):
        '''Get layout manager for children of item'''
        manager = None
        children = self.treeview.get_children(item)
        for child in children:
            if child != current:
                manager = self.treedata[child].manager
                break
        return manager
            
    
    def editor_edit(self, item, wdescr):
        self.current_edit = item
        manager_options = ['grid', 'pack', 'place']
        
        # Determine allowed manager options
        parent = self.treeview.parent(item)
        if parent:
            cm = self.get_children_manager(parent, item)
            if 'grid' == cm:
                manager_options.remove('pack')
            if 'pack' == cm:
                manager_options.remove('grid')
        logger.debug(manager_options)
        
        self.properties_editor.edit(wdescr)
        self.layout_editor.edit(wdescr, manager_options)
        self.bindings_editor.edit(wdescr)

    def editor_hide_all(self):
        self.properties_editor.hide_all()
        self.layout_editor.hide_all()
        self.bindings_editor.hide_all()

    def config_filter(self):
        def on_filtervar_changed(varname, element, mode):
            self.filter_by(self.filtervar.get())

        self.filtervar.trace('w', on_filtervar_changed)

        def on_filterbtn_click():
            self.filtervar.set('')

        self.filter_btn.configure(command=on_filterbtn_click)

    def config_treeview(self):
        """Sets treeview columns and other params"""
        tree = self.treeview
        tree.bind('<Double-1>', self.on_treeview_double_click)
        tree.bind('<<TreeviewSelect>>', self.on_treeview_select, add='+')

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
            self.filter_remove(remember=True)
            
            selected_id = self.treedata[item].identifier
            item = self.get_toplevel_parent(item)
            widget_id = self.treedata[item].identifier
            wclass = self.treedata[item].classname
            uidef = self.tree_to_uidef(item)
            
            self.previewer.draw(item, widget_id, uidef, wclass)
            self.previewer.show_selected(item, selected_id)
            self.filter_restore()

    def on_preview_in_toplevel(self, event=None):
        tv = self.treeview
        sel = tv.selection()
        if sel:
            self.filter_remove(remember=True)
            item = sel[0]
            item = self.get_toplevel_parent(item)
            widget_id = self.treedata[item].identifier
            uidef = self.tree_to_uidef(item)
            self.previewer.preview_in_toplevel(item, widget_id, uidef)
            self.filter_restore()
        else:
            logger.warning(_('No item selected.'))

    def on_treeview_double_click(self, event):
        tv = self.treeview
        sel = tv.selection()
        # toplevel_items = tv.get_children()
        if sel:
            item = sel[0]
            if tv.parent(item) == '':
                # only redraw if toplevel is double clicked
                self.draw_widget(item)

    def on_treeview_delete_selection(self, event=None):
        """Removes selected items from treeview"""

        tv = self.treeview
        selection = tv.selection()

        # Need to remove filter
        self.filter_remove(remember=True)

        toplevel_items = tv.get_children()
        parents_to_redraw = set()
        final_focus = None
        for item in selection:
            try:
                parent = ''
                if item not in toplevel_items:
                    parent = self.get_toplevel_parent(item)
                else:
                    self.previewer.delete(item)
                # determine final focus
                if final_focus is None:
                    candidates = (tv.prev(item), tv.next(item), tv.parent(item))
                    for c in candidates:
                        if c and (c not in selection):
                            final_focus = c
                            break
                # remove item
                del self.treedata[item]
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
            tv.after_idle(lambda: tv.selection_set(final_focus))
            tv.after_idle(lambda: tv.focus(final_focus))
            tv.after_idle(lambda: tv.see(final_focus))
            tv.after_idle(lambda i=final_focus,s=selected_id: self.previewer.show_selected(i, s))
        
        # restore filter
        self.filter_restore()
        
    def new_uidefinition(self):
        author = 'PygubuDesigner {0}'.format(pygubudesigner.__version__)
        uidef = UIDefinition(wmetaclass=WidgetMeta)
        uidef.author = author
        return uidef

    def tree_to_uidef(self, treeitem=None):
        """Traverses treeview and generates a ElementTree object"""

        # Need to remove filter or hidden items will not be saved.
        self.filter_remove(remember=True)
        
        uidef = self.new_uidefinition()
        if treeitem is None:
            items = self.treeview.get_children()
            for item in items:
                node = self.build_uidefinition(uidef, '', item)
                uidef.add_xmlnode(node)
        else:
            node = self.build_uidefinition(uidef, '', treeitem)
            uidef.add_xmlnode(node)

        # restore filter
        self.filter_restore()

        return uidef

    def build_uidefinition(self, uidef, parent, item):
        """Traverses tree and build ui definition"""

        node = uidef.widget_to_xmlnode(self.treedata[item])

        children = self.treeview.get_children(item)
        for child in children:
            child_node = self.build_uidefinition(uidef, item, child)
            uidef.add_xmlchild(node, child_node)
        return node

    def _insert_item(self, root, data, from_file=False):
        """Insert a item on the treeview and fills columns from data"""

        data.setup_defaults() # load default settings for properties and layout
        tree = self.treeview
        treelabel = '{0}: {1}'.format(data.identifier, data.classname)
        row = col = ''
        if root != '' and data.has_layout_defined():
            if data.manager == 'grid':
                row = data.layout_property('row')
                col = data.layout_property('column')
                # fix row position when using copy and paste
                # If collision, increase by 1
                row_count = self.get_max_row(root)
                if not from_file and (row_count > int(row) and int(col) == 0):
                    row = str(row_count + 1)
                    data.layout_property('row', row)

        image = ''
        try:
            image = StockImage.get('16x16-tk.default')
        except StockImageException:
            # TODO: notify something here
            pass

        try:
            image = StockImage.get('16x16-{0}'.format(data.classname))
        except StockImageException:
            # TODO: notify something here
            pass

        values = (data.classname, row, col)
        item = tree.insert(root, 'end', text=treelabel, values=values,
                           image=image)
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
        logger.debug('Selection %s', selection)
        if selection:
            self.filter_remove(remember=True)
            
            uidef = self.new_uidefinition()
            for item in selection:
                node = self.build_uidefinition(uidef, '', item)
                uidef.add_xmlnode(node)
            text = str(uidef)
            tree.clipboard_clear()
            tree.clipboard_append(text)
            self.filter_restore()

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
            if allowed_children:
                if classname not in allowed_children:
                    if show_warnings:
                        str_children = ', '.join(allowed_children)
                        msg = _('Allowed children: %s.')
                        logger.warning(msg, str_children)
                    is_valid = False
                    return is_valid

            children_count = len(self.treeview.get_children(root))
            maxchildren = root_boclass.maxchildren
            if maxchildren is not None and children_count >= maxchildren:
                if show_warnings:
                    msg = trlog(_('Only {0} children allowed for {1}'),
                                maxchildren, root_classname)
                    logger.warning(msg)
                is_valid = False
                return is_valid

            allowed_parents = new_boclass.allowed_parents
            if (allowed_parents is not None and
               root_classname not in allowed_parents):
                if show_warnings:
                    msg = trlog(_('{0} not allowed as parent of {1}'),
                                root_classname, classname)
                    logger.warning(msg)
                is_valid = False
                return is_valid

            if allowed_children is None and root_boclass.container is False:
                if show_warnings:
                    msg = _('Not allowed, %s is not a container.')
                    logger.warning(msg, root_classname)
                is_valid = False
                return is_valid

        else:
            # allways show warning when inserting in top level
            # if insertion is at top level,
            # Validate if it can be added at root level
            allowed_parents = new_boclass.allowed_parents
            if allowed_parents is not None and 'root' not in allowed_parents:
                if show_warnings:
                    msg = _('%s not allowed at root level')
                    logger.warning(msg, classname)
                is_valid = False
                return is_valid

            # if parents are not specified as parent,
            # check that item to insert is a container.
            # only containers are allowed at root level
            if new_boclass.container is False:
                if show_warnings:
                    msg = _('Not allowed at root level, %s is not a container.')
                    logger.warning(msg, classname)
                is_valid = False
                return is_valid
        return is_valid

    def _is_unique_id(self, root, widget_id):
        unique = True
        if root != '':
            data = self.treedata[root]
            if data.identifier == widget_id:
                unique = False
        if unique is True:
            for item in self.treeview.get_children(root):
                unique = self._is_unique_id(item, widget_id)
                if unique is False:
                    break
        return unique

    def _generate_id(self, classname, index):
        class_base_name = classname.split('.')[-1]
        name = class_base_name
        name = '{0}{1}'.format(name, index)
        if pref.get_option('widget_naming_separator') == 'UNDERSCORE':
            name = '{0}_{1}'.format(name, index)
        name = name.lower()
        if pref.get_option('widget_naming_ufletter') == 'yes':
            name = name.capitalize()
        return name

    def get_unique_id(self, classname, start_id=None):
        if start_id is None:
            self.counter[classname] += 1
            start_id = self._generate_id(classname, self.counter[classname])

        is_unique = self._is_unique_id('', start_id)
        while is_unique is False:
            self.counter[classname] += 1
            start_id = self._generate_id(classname, self.counter[classname])
            is_unique = self._is_unique_id('', start_id)
        
        return start_id

    def paste_from_clipboard(self):
        self.filter_remove(remember=True)
        
        tree = self.treeview
        selected_item = ''
        selection = tree.selection()
        if selection:
            selected_item = selection[0]
        try:
            text = tree.selection_get(selection='CLIPBOARD')
            
            uidef = self.new_uidefinition()
            uidef.load_from_string(text)
            for wmeta in uidef.widgets():
                if self._validate_add(selected_item, wmeta.classname):
                    self.update_layout(selected_item, wmeta)
                    self.populate_tree(selected_item, uidef, wmeta)
        except ET.ParseError:
            msg = 'The clipboard does not have a valid widget xml definition.'
            logger.error(msg)
        except tk.TclError:
            pass
        
        if selected_item == '':
            # redraw all
            children = tree.get_children('')
            for child in children:
                self.draw_widget(child)
        else:
            self.draw_widget(selected_item)
            
        
        self.filter_restore()

    def update_layout(self, root, data):
        '''Removes layout info from element, when copied from clipboard.'''
        
        cmanager = self.get_children_manager(root)
        cmanager = cmanager if cmanager is not None else self.default_layout_manager
        emanager = data.manager
        if emanager != 'place' and cmanager != emanager:
            data.manager = cmanager
    
    def add_widget(self, wclass):
        """Adds a new item to the treeview."""

        tree = self.treeview
        #  get the selected item:
        selected_item = ''
        tsel = tree.selection()
        if tsel:
            selected_item = tsel[0]

        #  Need to remove filter if set
        self.filter_remove()

        root = selected_item
        #  check if the widget can be added at selected point
        parent = tree.parent(root)
        has_parent = (parent != root)
        show_warnings = False if has_parent else True
        if not self._validate_add(root, wclass, show_warnings):
            #  if not try to add at item parent level
            parent = tree.parent(root)
            if parent != root:
                logger.info('Failed to add widget, trying one level up.')
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
        manager = self.default_layout_manager # << DEFAULT LAYOUT MANAGER
        if parent is not None:
            cmanager = self.get_children_manager(root)
            manager = cmanager if cmanager else manager
            
        widget_id = self.get_unique_id(wclass)
        pdefaults, ldefaults = WidgetMeta.get_widget_defaults(wclass, widget_id)
        data = WidgetMeta(wclass, widget_id, manager, pdefaults, ldefaults)
        
        # Recalculate position if manager is grid
        if manager == 'grid':
            rownum = '0'
            if root:
                rownum = str(self.get_max_row(root)+1)
            data.layout_property('row', rownum)
            data.layout_property('column', '0')

        item = self._insert_item(root, data)

        # Do redraw
        self.draw_widget(item)

        # Select and show the item created
        tree.after_idle(lambda: tree.selection_set(item))
        tree.after_idle(lambda: tree.focus(item))
        tree.after_idle(lambda: tree.see(item))

    def remove_all(self):
        self.treedata = {}
        self.filter_remove()
        children = self.treeview.get_children()
        if children:
            self.treeview.delete(*children)
        self.editor_hide_all()
        self.counter.clear() # Reset the widget counter (August 19, 2021)

    def load_file(self, filename):
        """Load file into treeview"""

        self.counter.clear()      
        uidef = UIDefinition(wmetaclass=WidgetMeta)
        uidef.load_file(filename)

        self.remove_all()
        self.previewer.remove_all()
        self.editor_hide_all()

        dirname = os.path.dirname(os.path.abspath(filename))
        self.previewer.resource_paths.append(dirname)
        for widget in uidef.widgets():
            self.populate_tree('', uidef, widget,from_file=True)
        
        children = self.treeview.get_children('')
        for child in children:
            self.draw_widget(child)
        self.previewer.show_selected(None, None)

    def populate_tree(self, master, uidef, wmeta, from_file=False):
        """Reads xml nodes and populates tree item"""

        cname = wmeta.classname
        original_id = wmeta.identifier
        uniqueid = self.get_unique_id(cname, wmeta.identifier)
        wmeta.widget_property('id', uniqueid)

        if cname in CLASS_MAP:
            pwidget = self._insert_item(master, wmeta, from_file=from_file)
            for mchild in uidef.widget_children(original_id):
                self.populate_tree(pwidget, uidef, mchild, from_file=from_file)
        else:
            raise Exception('Class "{0}" not mapped'.format(cname))

    def get_max_row(self, item):
        tree = self.treeview
        max_row = -1
        children = tree.get_children(item)
        for child in children:
            row = self.treedata[child].layout_property('row')
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

    def get_max_row_col(self, item):
        tree = self.treeview
        max_row = 0
        max_col = 0
        children = tree.get_children(item)
        for child in children:
            data = self.treedata[child]
            row = int(data.layout_property('row'))
            col = int(data.layout_property('column'))
            if row > max_row:
                max_row = row
            if col > max_col:
                max_col = col
        return (max_row, max_col)

    def update_event(self, hint, obj):
        """Updates tree colums when itemdata is changed."""
        
        if not self._listen_object_updates:
            return
        
        tree = self.treeview
        data = obj
        item = self.get_item_by_data(obj)
        item_text = '{0}: {1}'.format(data.identifier, data.classname)
        if item:
            if item_text != tree.item(item, 'text'):
                tree.item(item, text=item_text)
            # if tree.parent(item) != '' and 'layout' in data:
            if tree.parent(item) != '':
                if data.manager == 'grid':
                    row = data.layout_property('row')
                    col = data.layout_property('column')
                    values = tree.item(item, 'values')
                    if (row != values[1] or col != values[2]):
                        values = (data.classname, row, col)
                    tree.item(item, values=values)
            self.draw_widget(item)
            self.app.set_changed()

    def get_item_by_data(self, data):
        skey = None
        for key, value in self.treedata.items():
            if value == data:
                skey = key
                break
        return skey
    
    def on_item_nav_up(self, event=None):
        '''Move selection to prev item'''
        tree = self.treeview
        sel = tree.selection()
        if sel:
            item = sel[0]
            prev = tree.prev(item)
            if prev and tree.item(prev, 'open'):
                children = tree.get_children(prev)
                if children:
                    prev = children[-1]
            if not prev:
                prev = tree.parent(item)
            if prev:
                tree.selection_set(prev)
    
    def on_item_nav_down(self, event=None):
        '''Move selection to next item'''
        tree = self.treeview
        sel = tree.selection()
        if sel:
            item = sel[0]
            next_ = None
            if tree.item(item, 'open'):
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
            self.filter_remove(remember=True)
            item = sel[0]
            parent = tree.parent(item)
            prev = tree.prev(item)
            if prev:
                prev_idx = tree.index(prev)
                tree.move(item, parent, prev_idx)
                manager = self.treedata[item].manager
                self.app.set_changed()
                if manager in ('pack', 'place'):
                    self.draw_widget(item)
            self.filter_restore()

    def on_item_move_down(self, event):
        tree = self.treeview
        sel = tree.selection()
        if sel:
            self.filter_remove(remember=True)
            item = sel[0]
            parent = tree.parent(item)
            next = tree.next(item)
            if next:
                next_idx = tree.index(next)
                tree.move(item, parent, next_idx)
                manager = self.treedata[item].manager
                self.app.set_changed()
                if manager in ('pack', 'place'):
                    self.draw_widget(item)
            self.filter_restore()

    #
    # Item grid move functions
    #
    def on_item_grid_move(self, direction):
        tree = self.treeview
        selection = tree.selection()
        if selection:
            item_first = selection[0]
            self.filter_remove(remember=True)
            for item in selection:
                data = self.treedata[item]
                
                if data.manager != 'grid':
                    break

                if direction == self.GRID_UP:
                    row = int(data.layout_property('row'))
                    if row > 0:
                        row = row - 1
                        data.layout_property('row', str(row))
                        data.notify()
                elif direction == self.GRID_DOWN:
                    row = int(data.layout_property('row'))
                    row = row + 1
                    data.layout_property('row', str(row))
                    data.notify()
                elif direction == self.GRID_LEFT:
                    column = int(data.layout_property('column'))
                    if column > 0:
                        column = column - 1
                        data.layout_property('column', str(column))
                        data.notify()
                elif direction == self.GRID_RIGHT:
                    column = int(data.layout_property('column'))
                    column = column + 1
                    data.layout_property('column', str(column))
                    data.notify()
                root = tree.parent(item)
            self.filter_restore()
            self.editor_edit(item_first, self.treedata[item_first])

    #
    # Filter functions
    #
    def filter_by(self, string):
        """Filters treeview"""

        self._reatach()
        if string == '':
            self.filter_remove()
            return

        self._expand_all()
        self.treeview.selection_set('')

        children = self.treeview.get_children('')
        for item in children:
            _, detached = self._detach(item)
            if detached:
                self._detached.extend(detached)
        for i, p, idx in self._detached:
            # txt = self.treeview.item(i, 'text')
            self.treeview.detach(i)
        self.filter_on = True

    def filter_remove(self, remember=False):
        if self.filter_on:
            sitem = None
            selection = self.treeview.selection()
            if selection:
                sitem = selection[0]
                self.treeview.after_idle(lambda: self._see(sitem))
            if remember:
                self.filter_prev_value = self.filtervar.get()
                self.filter_prev_sitem = sitem
            self._reatach()
            self.filtervar.set('')
        self.filter_on = False

    def filter_restore(self):
        if self.filter_prev_value:
            self.filtervar.set(self.filter_prev_value)
            item = self.filter_prev_sitem
            if item and self.treeview.exists(item):
                self.treeview.selection_set(item)
                self.treeview.after_idle(lambda: self._see(item))
            # clear
            self.filter_prev_value = ''
            self.filter_prev_sitem = None

    def _see(self, item):
        # The item may have been deleted.
        try:
            self.treeview.see(item)
        except tk.TclError:
            pass

    def _expand_all(self, rootitem=''):
        children = self.treeview.get_children(rootitem)
        for item in children:
            self._expand_all(item)
        if rootitem != '' and children:
            self.treeview.item(rootitem, open=True)

    def _reatach(self):
        """Reinsert the hidden items."""
        for item, p, idx in self._detached:
            # The item may have been deleted.
            if self.treeview.exists(item) and self.treeview.exists(p):
                self.treeview.move(item, p, idx)
        self._detached = []

    def _detach(self, item):
        """Hide items from treeview that do not match the search string."""
        to_detach = []
        children_det = []
        children_match = False
        match_found = False

        value = self.filtervar.get()
        txt = self.treeview.item(item, 'text').lower()
        if value in txt:
            match_found = True
        else:
            class_txt = self.treedata[item].classname.lower()
            if value in class_txt:
                match_found = True

        parent = self.treeview.parent(item)
        idx = self.treeview.index(item)
        children = self.treeview.get_children(item)
        if children:
            for child in children:
                match, detach = self._detach(child)
                children_match = children_match | match
                if detach:
                    children_det.extend(detach)

        if match_found:
            if children_det:
                to_detach.extend(children_det)
        else:
            if children_match:
                if children_det:
                    to_detach.extend(children_det)
            else:
                to_detach.append((item, parent, idx))
        match_found = match_found | children_match
        return match_found, to_detach

    #
    # End Filter functions
    #
    
    def get_topwidget_list(self):
        wlist = []
        children = self.treeview.get_children('')
        for item in children:
            data = self.treedata[item]
            label = u'{0} ({1})'.format(data.identifier, data.classname)
            element = (item, label)
            wlist.append(element)
        return wlist
    
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
            self.filter_remove()
            self._expand_all()
            tree.after_idle(lambda: tree.selection_set(found))
            tree.after_idle(lambda: tree.focus(found))
            tree.after_idle(lambda: tree.see(found))
    
    def is_id_unique(self, idvalue):
        "Check if idvalue is unique in all UI tree."
        # Used in ID validation
        return self._is_unique_id('', idvalue)
    

