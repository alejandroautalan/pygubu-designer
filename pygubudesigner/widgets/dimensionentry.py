# encoding: UTF-8
#
# Copyright 2012-2017 Alejandro Autalán
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
import re

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

from pygubudesigner.widgets.propertyeditor import *


RE_DIMENSION = re.compile('(\d+([cimp])?)?$')
RE_TWO_DIMENSION = re.compile('(\d+([cimp])?|\d+([cimp])?\s\d+([cimp])?)?$')


class DimensionPropertyEditor(EntryPropertyEditor):
    REGEX = RE_DIMENSION
    def __init__(self, master=None, **kw):
        self._empty_data = None
        EntryPropertyEditor.__init__(self, master, **kw)
    
    def _validate(self):
        valid = False
        value = self._get_value()
        m = self.REGEX.match(value)
        if m:
            valid = True
        self.show_invalid(not valid)
        return valid
    
    def _get_value(self):
        value = self._variable.get()
        
        if self._empty_data is not None and value == '':
            value = str(self._empty_data)
            self._set_value(value)
        
        return value
    
    def parameters(self, **kw):
        pvalue = kw.pop('empty_data', None)
        self._empty_data = None if pvalue is None else pvalue
        EntryPropertyEditor.parameters(self, **kw)


class TwoDimensionPropertyEditor(DimensionPropertyEditor):
    REGEX = RE_TWO_DIMENSION


register_editor('dimensionentry', DimensionPropertyEditor)
register_editor('twodimensionentry', TwoDimensionPropertyEditor)


if __name__ == '__main__':
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    def make_on_change_cb(editor):
        def on_change_cb(event=None):
            print(editor.value)
            print(repr(editor.value))
        return on_change_cb

    editor = DimensionPropertyEditor(root)
    editor.pack(expand=True, fill='x')
    editor.edit('10m')
    editor.bind('<<PropertyChanged>>', make_on_change_cb(editor))
    
    editor2 = TwoDimensionPropertyEditor(root)
    editor2.pack(expand=True, fill='x')
    editor2.edit('10p 20p')
    editor2.bind('<<PropertyChanged>>', make_on_change_cb(editor2))    

    root.mainloop()
