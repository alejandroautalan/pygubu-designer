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

from __future__ import unicode_literals
from collections import OrderedDict
import json

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

from pygubu.builder.builderobject import CB_TYPES
from pygubudesigner.i18n import translator as _
from pygubudesigner.widgets import EntryPropertyEditor
from pygubudesigner.widgets.propertyeditor import register_editor
from pygubudesigner.widgets.commandentry import CommandPropertyBase


class EntryValidateCommandPropertyEditor(CommandPropertyBase):
    
    def _create_ui(self):
        self._cbname = w = EntryPropertyEditor(self)
        w.grid(row=0, column=0, sticky='nswe', columnspan=2)
        w.bind('<<PropertyChanged>>', self._on_variable_changed)
        
        self._arg_var = var = tk.StringVar(self, '')
        self._argd = w = EntryPropertyEditor(self)
        w.parameters(state='readonly', textvariable=var)
        w.grid(row=1, column=0, sticky='nswe')
        
        self._mb = w = ttk.Menubutton(self, text='Args')
        w.grid(row=1, column=1, sticky='nswe')
        
        olist = (
            ('%d', _('Type of action.')),
            ('%i', _('Index of character string to be inserted/deleted.')),
            ('%P', _("The new/current value of the entry.")),
            ('%s', _('The current value of entry prior to editing.')),
            ('%S', _('The text string being inserted/deleted.')),
            ('%v', _('The current value of the -validate option.')),
            ('%V', _('The validation condition that triggered the callback.')),
            ('%W', _('The name of the entry widget.')),
        )
        options = OrderedDict(olist)
        self._vars = { k: tk.BooleanVar(self) for k in options.keys() }
        
        self._menu = m = tk.Menu(self._mb, tearoff=False)
        m.add_command(label=_('Select all'), command=self._on_select_all)
        m.add_command(label=_('Clear'), command=self._on_clear)
        m.add_separator()
        for key, txt in options.items():
            txt = '{0} {1}'.format(key, txt)
            m.add_checkbutton(label=txt, variable=self._vars[key],
                              command=self._on_update_args)
        self._mb['menu'] = m
        self.columnconfigure(0, weight=1)
    
    def _on_select_all(self):
        for key, var in self._vars.items():
            var.set(True)
        self._on_update_args()
        self._on_variable_changed()
    
    def _on_clear(self):
        for key, var in self._vars.items():
            var.set(False)
        self._on_update_args()
        self._on_variable_changed()
    
    def _on_update_args(self, event=None):
        self._arg_var.set(self._get_args())
        self._on_variable_changed()
    
    def _get_args(self):
        args = []
        for key, var in self._vars.items():
            if var.get():
                args.append(key)
        args = ' '.join(args)
        return args
    
    def _set_args(self, args):
        arglist = args.split(' ')
        for key, var in self._vars.items():
            var.set(False)
            if key in arglist:
                var.set(True)
    
    def _set_value(self, value):
        """Save value on storage"""
        cbname = ''
        args = ''
        if len(value) != 0:
            vd = json.loads(value)
            cbname = vd['value']
            args = vd['args']
        self._cbname.edit(cbname)
        self._set_args(args)
        self._arg_var.set(self._get_args())
        self._variable.set(value)
    
    def _get_value(self):
        value = ''
        if len(self._cbname.value) != 0:
            args = self._get_args()
            cmd = {
                'type': 'command',
                'value': self._cbname.value,
                'cbtype': CB_TYPES.ENTRY_VALIDATE,
                'args': args,
            }
            value = json.dumps(cmd)
        return value
    
    def _validate(self):
        is_valid = True
        value = self._cbname.value
        if len(value) != 0:
            is_valid = self.is_safe_identifier(value)
        self.show_invalid(not is_valid)
        return is_valid

register_editor('entryvalidatecommandentry', EntryValidateCommandPropertyEditor)


if __name__ == '__main__':
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    editor = EntryValidateCommandPropertyEditor(root)
    editor.grid(sticky='nsew')
    
    def on_change_cb(self, event=None):
        print('change cb')
        print(editor.value)
    
    editor.bind('<<PropertyChanged>>', on_change_cb)
    value = '{"value":"mycb", "cbtype": "entryvalidate"}'
    editor.edit(value)
    
    root.mainloop()