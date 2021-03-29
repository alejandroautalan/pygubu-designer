# encoding: UTF-8
#
# Copyright 2012-2021 Alejandro Autalán
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

from __future__ import unicode_literals, print_function
import logging

try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import messagebox
except:
    import Tkinter as tk
    import ttk
    import tkMessageBox as messagebox

from pygubu import builder
from pygubu.widgets.simpletooltip import create as create_tooltip
from pygubudesigner.widgets.propertyeditor import (create_editor,
    LayoutManagerPropertyEditor)
from pygubudesigner import properties
from pygubudesigner.i18n import translator as _
from pygubudesigner.propertieseditor import PropertiesEditor

logger = logging.getLogger(__name__)
CLASS_MAP = builder.CLASS_MAP


class LayoutEditor(PropertiesEditor):
    managers_keys = ('grid', 'pack', 'place')
    managers_labels = (_('Grid'), _('Pack'), _('Place'))
    managers = dict(zip(managers_keys, managers_labels))

    def _create_properties(self):
        """Populate a frame with a list of all editable properties"""
        
        # Layout selector
        self._fselector = fm = ttk.Frame(self._sframe.innerframe)
        label = ttk.Label(fm, text='Manager:')
        label.pack(side='left')
        self.layout_selector = combo = LayoutManagerPropertyEditor(fm)
        combo.parameters(state='readonly', values=self.managers)
        combo.pack(side='left', expand=True)
        combo.bind('<<PropertyChanged>>', self._layout_manager_changed)
        self._allowed_managers = self.managers.keys()
        fm.grid(row=0, sticky='w')
        
        # Layout Options editors
        self._rcbag = {}  # bag for row/column prop editors
        # main options frame
        self._fprop = f = ttk.Labelframe(self._sframe.innerframe,
                                         text=_('Options:'), padding=4)
        f.grid(row=1, sticky='nswe')
        #  hack to resize correctly when properties are hidden
        label = ttk.Frame(f)
        label.grid()

        label_tpl = "{0}:"
        row = 0
        col = 0

        groups = (
            ('00', properties.MANAGER_PROPERTIES, properties.LAYOUT_OPTIONS),
        )

        for gcode, plist, propdescr in groups:
            for name in plist:
                kwdata = propdescr[name]
                labeltext = label_tpl.format(name)
                label = ttk.Label(self._fprop, text=labeltext, anchor=tk.W)
                label.grid(row=row, column=col, sticky=tk.EW, pady=2)
                label.tooltip = create_tooltip(label, '?')
                widget = self._create_editor(self._fprop, name, kwdata)
                widget.grid(row=row, column=col+1, sticky=tk.EW, pady=2)
                row += 1
                self._propbag[gcode+name] = (label, widget)

        # Grid row properties
        self._fgr_label = _("Grid row '{0}' options:")
        self._fgr = fgr = ttk.LabelFrame(self._sframe.innerframe,
                                        text=self._fgr_label,
                                        padding=5)
        fgr.grid(row=2, column=0, sticky=tk.NSEW, pady='10 0')
        name_format = 'row_{0}'  # row_{name}
        row = 0
        label_tpl = "{0}:"
        for pname in properties.GRID_RC_PROPERTIES:
            kwdata = properties.LAYOUT_OPTIONS[pname]
            alias = name_format.format(pname)
            labeltext = label_tpl.format(pname)
            label = ttk.Label(fgr, text=labeltext, anchor=tk.W)
            label.grid(row=row, column=0, sticky=tk.EW, pady=2)
            label.tooltip = create_tooltip(label, '?')
            
            widget = self._create_editor(fgr, alias, kwdata)
            widget.grid(row=row, column=1, sticky=tk.EW, pady=2)
            self._rcbag[alias] = (label, widget)
            row = row + 1
        fgr.columnconfigure(1, weight=1)
        
        # Grid column properties
        self._fgc_label = _("Grid column '{0}' options:")
        self._fgc = fgc = ttk.LabelFrame(self._sframe.innerframe,
                                           text=self._fgc_label,
                                           padding=5)
        fgc.grid(row=3, column=0, sticky=tk.NSEW, pady='10 0')
        name_format = 'col_{0}'  # row_{name}
        row = 0
        label_tpl = "{0}:"
        for pname in properties.GRID_RC_PROPERTIES:
            kwdata = properties.LAYOUT_OPTIONS[pname]
            alias = name_format.format(pname)
            labeltext = label_tpl.format(pname)
            label = ttk.Label(fgc, text=labeltext, anchor=tk.W)
            label.grid(row=row, column=0, sticky=tk.EW, pady=2)
            label.tooltip = create_tooltip(label, '?')
            
            widget = self._create_editor(fgc, alias, kwdata)
            widget.grid(row=row, column=1, sticky=tk.EW, pady=2)
            self._rcbag[alias] = (label, widget)
            row = row + 1
        fgc.columnconfigure(1, weight=1)

    
    def edit(self, wdescr, manager_options):
        self._current = wdescr

        wclass = wdescr.classname
        #class_descr = CLASS_MAP[wclass].builder
        max_children = CLASS_MAP[wclass].builder.maxchildren
        max_children = 0 if max_children is None else max_children
        is_container = CLASS_MAP[wclass].builder.container
        layout_required = CLASS_MAP[wclass].builder.layout_required
        show_layout = layout_required

        self._fprop.grid()
        self._fselector.grid()
        # manager selector
        manager = wdescr.manager
        manager_prop = properties.GRID_PROPERTIES
        if manager == 'pack':
            manager_prop = properties.PACK_PROPERTIES
        elif manager == 'place':
            manager_prop = properties.PLACE_PROPERTIES
        
        if show_layout:
            self._allowed_managers = manager_options
            self.layout_selector.edit(manager)
            self.layout_selector.pack()
        else:
            self.layout_selector.pack_forget()
        
        #layout properties
        groups = (
            ('00', properties.MANAGER_PROPERTIES, properties.LAYOUT_OPTIONS),
        )

        for gcode, proplist, gproperties in groups:
            for name in proplist:
                propdescr = gproperties[name]
                label, widget = self._propbag[gcode + name]
                if show_layout and name in manager_prop:
                    self.update_editor(label, widget, wdescr, name, propdescr)
                    label.grid()
                    widget.grid()
                else:
                    label.grid_remove()
                    widget.grid_remove()

        # determine if show grid r/c properties
        show_grid_rc = (manager == 'grid' and layout_required)

        if show_grid_rc:
            rownum = wdescr.layout_property('row')
            colnum = wdescr.layout_property('column')
            label = self._fgr_label.format(rownum)
            self._fgr.config(text=label)
            label = self._fgc_label.format(colnum)
            self._fgc.config(text=label)
            
            target = self._current
            for key in self._rcbag:
                rowcol, name = self.identify_gridrc_property(key)
                propdescr = properties.LAYOUT_OPTIONS[name]
                number = colnum if rowcol == 'col' else rownum
                label, widget = self._rcbag[key]
                self.update_rc_editor(rowcol, number, label, widget,
                                      target, name, propdescr)
            self._fgr.grid()
            self._fgc.grid()
        else:
            self._fgr.grid_remove()
            self._fgc.grid_remove()

        self._sframe.reposition()

    def _layout_manager_changed(self, event=None):
        if self._current is None:
            # I'm not editing anything
            return
        
        old_manager = self._current.manager
        new_manager = self.layout_selector.value
        needs_container_change = (new_manager not in self._allowed_managers)
        
        if needs_container_change:
            self.layout_selector.edit(old_manager)
            cb = lambda f=old_manager,t=new_manager: self._ask_manager_change(f, t)
            self._fselector.after_idle(cb)
        else:
            self._current.manager = new_manager
            self.edit(self._current, self._allowed_managers)
    
    def _ask_manager_change(self, old_manager, new_manager):
        title = _('Change Manager')
        msg = _('Change manager from {0} to {1}?')
        msg = msg.format(old_manager, new_manager)
        detail = _('All container widgets will be updated.')
        user_accepts_change = messagebox.askokcancel(
            title, msg, detail=detail,
            parent=self.layout_selector.winfo_toplevel())
        if user_accepts_change:
            topack = '<<LayoutEditorContainerManagerToPack>>'
            togrid = '<<LayoutEditorContainerManagerToGrid>>'
            event_name = togrid if new_manager == 'grid' else topack
            self._fselector.event_generate(event_name)
    
    def _on_property_changed(self, name, editor):
        value = editor.value
        if name in properties.MANAGER_PROPERTIES:
            self._current.layout_property(name, value)
        else:
            # asume that is a grid row/col property
            rowcol, pname = self.identify_gridrc_property(name)
            number = self._current.layout_property('row')
            if rowcol == 'col':
                number = self._current.layout_property('column')
            target = self._current
            target.gridrc_property(rowcol, number, pname, value)
            editor.event_generate('<<LayoutEditorGridRCChanged>>')

    def identify_gridrc_property(self, alias):
        return alias.split('_')

    def update_editor(self, label, editor, wdescr, pname, propdescr):
        pdescr = propdescr.copy()
        manager = wdescr.manager

        if manager in pdescr:
            pdescr = dict(pdescr, **pdescr[manager])

        label.tooltip.text = pdescr.get('help', None)
        params = pdescr.get('params', {})
        editor.parameters(**params)
        default = pdescr.get('default', '')

        value = wdescr.layout_property(pname)
        if not value and default:
            value = default
        editor.edit(value)

    def update_rc_editor(self, type_, index, label, editor, wdescr, pname, propdescr):
        pdescr = propdescr.copy()
        classname = wdescr.classname

        if classname in pdescr:
            pdescr = dict(pdescr, **pdescr[classname])

        label.tooltip.text = pdescr.get('help', None)
        params = pdescr.get('params', {})
        editor.parameters(**params)
        default = pdescr.get('default', '')

        value = ''
        value = wdescr.gridrc_property(type_, str(index), pname)
        if not value and default:
            value = default
        editor.edit(value)

    def hide_all(self):
        super(LayoutEditor, self).hide_all()
        self._fselector.grid_remove()
        self._fprop.grid_remove()
        self._fgr.grid_remove()
        self._fgc.grid_remove()
        

