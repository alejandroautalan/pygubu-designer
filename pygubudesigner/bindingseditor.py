# encoding: UTF-8
#
# Copyright 2012-2014 Alejandro Autalán
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
try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

from pygubu import builder

CLASS_MAP = builder.CLASS_MAP


class BindingsEditor:
    def __init__(self, etreeview, parent):
        self.tv = etreeview
        self._curr_data = None
        self._curr_bo = None
        self._adder = 'adder'
        self._allow_edit = False
        self._parent = parent
        self.tv.insert('', tk.END, iid=self._adder, values=('+',))
        self.tv.bind('<<TreeviewInplaceEdit>>', self._on_inplace_edit)
        self.tv.bind('<<TreeviewCellEdited>>', self._on_cell_edited)
        self.tv.bind('<Double-Button-1>', self._on_add_clicked, add=True)

        self._del_btn = ttk.Button(self.tv, text='-',
                                   command=self._on_del_clicked)
        self._seq_cboxvar = tk.StringVar()
        self._seq_cbox = cbox = ttk.Combobox(self.tv,
                                             textvariable=self._seq_cboxvar)
        #cbox.place(x=-10, y=-10)
        self.hide_all()

    def _on_add_clicked(self, event):
#        print('_on_add_clicked')
        sel = self.tv.selection()
        if sel:
            item = sel[0]
            if item == self._adder and self._allow_edit:
                self._add_binding(('<1>', 'callback', ''))

    def _on_del_clicked(self):
        sel = self.tv.selection()
        if sel:
            item = sel[0]
            self.tv.delete(item)
        self._copy_to_data()

    def _on_cell_edited(self, event):
        col, item = self.tv.get_event_info()
        self._copy_to_data()

    def _copy_to_data(self):
        if self._curr_data is not None:
            items = self.tv.get_children()
            self._curr_data.clear_bindings()
            for item in items:
                if item != self._adder:
                    values = self.tv.item(item, 'values')
#                    print(item, 'values = ', values)
                    self._curr_data.add_binding(*values[:3])
                    self._curr_data.notify(self)

    def _add_binding(self, bind):
        idx = self.tv.index(self._adder)
        self.tv.insert('', idx, values=bind)
        self.tv.selection_set('')

    def edit(self, wdescr):
        wclass = wdescr.classname
        self.clear()
        self._curr_data = wdescr
        self._curr_bo = CLASS_MAP[wclass].builder
        self._seq_cbox.config(values=self._curr_bo.virtual_events)
        
        self._allow_edit = self._curr_bo.allow_bindings
        if self._allow_edit:
            self._parent.pack(fill='both', expand='True')
        else:
            self._parent.pack_forget()
        
        for bind in wdescr.bindings:
            self._add_binding(bind)

    def _on_inplace_edit(self, event):
        col, item = self.tv.get_event_info()
        if item != self._adder and self._allow_edit:
            if col == 'sequence':
                self.tv.inplace_custom(col, item, self._seq_cbox,
                                       self._seq_cboxvar)
            elif col == 'handler':
                self.tv.inplace_entry(col, item)
            elif col == 'add':
                self.tv.inplace_checkbutton(col, item, offvalue='')
            elif col == 'actions':
                self.tv.inplace_custom(col, item, self._del_btn)
    
    def hide_all(self):
        self._parent.pack_forget()

    def clear(self):
        children = self.tv.get_children()
        for item in children:
            if item != self._adder:
                self.tv.delete(item)
