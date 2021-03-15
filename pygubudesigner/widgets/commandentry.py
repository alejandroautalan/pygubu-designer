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
import keyword
import re
import json

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

from pygubu.builder.builderobject import CB_TYPES
from pygubudesigner.i18n import translator as _
from pygubudesigner.widgets.propertyeditor import *


class CommandPropertyBase(PropertyEditor):
    RE_IDENTIFIER = re.compile('[_A-Za-z][_a-zA-Z0-9]*$')
    
    def is_safe_identifier(self, value):
        is_valid = True
        if keyword.iskeyword(value):
            is_valid = False
        if is_valid and not self.RE_IDENTIFIER.match(value):
            is_valid = False
        return is_valid


class SimpleCommandEntry(CommandPropertyBase):
    cmd_type = CB_TYPES.SIMPLE
    
    def _create_ui(self):
        self._cbname = w = EntryPropertyEditor(self)
        w.grid(row=0, column=0, sticky='nswe', columnspan=2)
        w.bind('<<PropertyChanged>>', self._on_variable_changed)
        self.columnconfigure(0, weight=1)
    
    def _set_value(self, value):
        """Save value on storage"""
        cbname = ''
        if len(value) != 0:
            vd = json.loads(value)
            cbname = vd['value']
        self._cbname.edit(cbname)
        self._variable.set(value)
    
    def _get_value(self):
        value = ''
        if len(self._cbname.value) != 0:
            cmd = {
                'type': 'command',
                'value': self._cbname.value,
                'cbtype': self.cmd_type
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


class ScrollCommandEntry(SimpleCommandEntry):
    cmd_type = CB_TYPES.SCROLL


class ScrollSetCommandEntry(SimpleCommandEntry):
    cmd_type = CB_TYPES.SCROLLSET


class ScaleCommandEntry(SimpleCommandEntry):
    cmd_type = CB_TYPES.SCALE


register_editor('simplecommandentry', SimpleCommandEntry)
register_editor('scrollcommandentry', ScrollCommandEntry)
register_editor('scrollsetcommandentry', ScrollSetCommandEntry)
register_editor('scalecommandentry', ScaleCommandEntry)


class CommandPropertyEditor(CommandPropertyBase):
    
    def _create_ui(self):
        self._lbl_callback = _('Callback:')
        self._plabel = w = ttk.Label(self, text=self._lbl_callback,
                                     font='TkSmallCaptionFont')
        w.grid(row=0, column=0, sticky='nswe')
        
        self._cbname = w = EntryPropertyEditor(self)
        w.grid(row=0, column=1, sticky='nswe')
        w.bind('<<PropertyChanged>>', self._on_variable_changed)
        # type label:
        w = ttk.Label(self, text='Type:', font='TkSmallCaptionFont')
        w.grid(row=1, column=0, sticky='nsew')
        # type combo
        cmdtypes = (
            (CB_TYPES.SIMPLE, _('Simple')),
            (CB_TYPES.WITH_WID, _('Send widget ID')),
        )
        self._cmdtype = w = ChoiceByKeyPropertyEditor(self)
        w.parameters(values=cmdtypes)
        w.bind('<<PropertyChanged>>', self._on_variable_changed)
        w.grid(row=1, column=1, sticky='nswe')
        self.columnconfigure(1, weight=1)
    
    def _set_value(self, value):
        """Save value on storage"""
        cbname = ''
        cbtype = CB_TYPES.SIMPLE
        if len(value) != 0:
            vd = json.loads(value)
            cbname = vd['value']
            cbtype = vd['cbtype']
        self._cbname.edit(cbname)
        self._cmdtype.edit(cbtype)
        self._variable.set(value)
    
    def _get_value(self):
        value = ''
        if len(self._cbname.value) != 0:
            cmd = {
                'type': 'command',
                'value': self._cbname.value,
                'cbtype': self._cmdtype.value
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


register_editor('commandentry', CommandPropertyEditor)



if __name__ == '__main__':
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    editor = CommandPropertyEditor(root)
    editor.grid(sticky='nsew')
    
    def change_cb(self, event=None):
        print('change cb')
    
    editor.bind('<<PropertyChanged>>', change_cb)
    value = '{"value":"mycb", "cbtype": "simple"}'
    editor.edit(value)

    root.mainloop()