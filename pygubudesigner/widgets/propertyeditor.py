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
#
# For further info, check  http://pygubu.web.here

from __future__ import unicode_literals

__all__ = ['PropertyEditor', 'EntryPropertyEditor', 'SpinboxPropertyEditor',
           'ChoicePropertyEditor', 'TextPropertyEditor',
           'CheckbuttonPropertyEditor', 'register_editor', 'create_editor']

import os
import keyword
import re

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

from pygubu.stockimage import StockImage, StockImageException
from pygubu.widgets.scrollbarhelper import ScrollbarHelper
from pygubu.widgets.combobox import Combobox

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(FILE_DIR, "..", "images", "widgets", "propertyeditor")
IMAGES_DIR = os.path.abspath(IMAGES_DIR)
StockImage.register_from_dir(IMAGES_DIR)

EDITORS = {}


def register_editor(name, class_):
    EDITORS[name] = class_


def create_editor(name, *args, **kw):
    editor = EDITORS[name](*args, **kw)
    return editor


class PropertyEditor(ttk.Frame):
    style_initialized = False
    
    def __init__(self, master=None, **kw):
        self._variable = tk.StringVar()
        self._initvalue = None
        self.value = ''
        ttk.Frame.__init__(self, master, **kw)
        
        if not PropertyEditor.style_initialized:
            s = ttk.Style()
            s.configure('PropertyEditorInvalid.TFrame', background='red')
        self.configure(borderwidth=2)
        self._create_ui()
        
    def show_invalid(self, invalid=True):
        if invalid:
            self.configure(style='PropertyEditorInvalid.TFrame')
        else:
            self.configure(style='TFrame')

    def _create_ui(self):
        pass

    def _validate(self):
        return True

    def _get_value(self):
        """Get value from storage"""
        return self._variable.get()

    def _set_value(self, value):
        """Save value on storage"""
        self._variable.set(value)

    def _on_variable_changed(self, event=None):
        if self._validate():
            self.value = self._get_value()
            if self.value != self._initvalue:
                self.event_generate('<<PropertyChanged>>')
                self._initvalue = self.value
                self._after_change()

    def _after_change(self):
        pass
    
    def parameters(self, **kw):
        pass

    def edit(self, value):
        self._initvalue = value
        self.value = value
        self._set_value(value)


class EntryPropertyEditor(PropertyEditor):
    def _create_ui(self):
        self._entry = entry = ttk.Entry(self, textvariable=self._variable)
        entry.grid(sticky='we')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        entry.bind('<FocusOut>', self._on_variable_changed)
        entry.bind('<KeyPress-Return>', self._on_variable_changed)
        entry.bind('<KeyPress-KP_Enter>', self._on_variable_changed)

    def parameters(self, **kw):
        self._entry.configure(**kw)


class AlphanumericEntryPropertyEditor(EntryPropertyEditor):
    def _validate(self):
        is_valid = True
        value = self._get_value()
        if len(value) != 0:
            is_valid = value.isalnum()
        self.show_invalid(not is_valid)
        return is_valid


class CommandEntryPropertyEditor(EntryPropertyEditor):
    RE_IDENTIFIER = re.compile('[_A-Za-z][_a-zA-Z0-9]*$')
    
    def _validate(self):
        is_valid = True
        value = self._get_value()
        if len(value) != 0:
            if keyword.iskeyword(value):
                is_valid = False
            if is_valid and not self.RE_IDENTIFIER.match(value):
                is_valid = False
        self.show_invalid(not is_valid)
        return is_valid


SpinboxClass = tk.Spinbox
if tk.TkVersion >= 8.6 and not hasattr(ttk, 'Spinbox'):
    from pygubu.widgets.ttkspinbox import Spinbox
    SpinboxClass = Spinbox


class SpinboxPropertyEditor(PropertyEditor):
    def _create_ui(self):
        self._spinbox = SpinboxClass(self, textvariable=self._variable,
                                     command=self._on_variable_changed)
        spinbox = self._spinbox
        spinbox.grid(sticky='we')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        spinbox.bind('<FocusOut>', self._on_variable_changed)
        spinbox.bind('<KeyPress-Return>', self._on_variable_changed)
        spinbox.bind('<KeyPress-KP_Enter>', self._on_variable_changed)

    def parameters(self, **kw):
        self._spinbox.configure(**kw)


class TextPropertyEditor(PropertyEditor):
    def _create_ui(self):
        self._sbh = ScrollbarHelper(self)
        self._sbh.grid(row=0, column=0, sticky='we')
        self._text = text = tk.Text(self._sbh.container, width=20, height=3)
        self._sbh.add_child(self._text)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        text.bind('<FocusOut>', self._on_variable_changed)

    def _get_value(self):
        value = self._text.get('0.0', tk.END)
        if value.endswith('\n'):
            value = value[:-1]
        return value

    def _set_value(self, value):
        self._text.delete('0.0', tk.END)
        self._text.insert('0.0', value)


class ChoicePropertyEditor(PropertyEditor):
    def _create_ui(self):
        self._cb_pending = False
        self._combobox = combobox = ttk.Combobox(self,
                                                 textvariable=self._variable)
        combobox.grid(sticky='we')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        sequenses = ('<FocusOut>', '<KeyPress-Return>',
                     '<KeyPress-KP_Enter>', '<<ComboboxSelected>>')
        for seq in sequenses:
            combobox.bind(seq, self._on_variable_changed)

    def parameters(self, **kw):
        self._combobox.configure(**kw)


class ChoiceByKeyPropertyEditor(ChoicePropertyEditor):
    def _create_ui(self):
        self._cb_pending = False
        self._combobox = combobox = Combobox(self, keyvariable=self._variable)
        combobox.grid(sticky='we')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        sequenses = ('<FocusOut>', '<KeyPress-Return>',
                     '<KeyPress-KP_Enter>', '<<ComboboxSelected>>')
        for seq in sequenses:
            combobox.bind(seq, self._on_variable_changed)


class CheckbuttonPropertyEditor(PropertyEditor):
    def _create_ui(self):
        self._checkb = w = ttk.Checkbutton(self, variable=self._variable)
        w.grid(sticky='we')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        w.configure(command=self._on_variable_changed)

    def parameters(self, **kw):
        self._checkb.configure(**kw)


class NaturalNumberEditor(EntryPropertyEditor):
    def _validate(self):
        valid = True
        value = self._get_value()
        if len(value) != 0:
            valid = False
            try:
                number = int(value)
                if number >= 0:
                    valid = True
            except:
                pass
        self.show_invalid(not valid)
        return valid


class IntegerNumberEditor(EntryPropertyEditor):
    def _validate(self):
        valid = True
        value = self._get_value()
        if len(value) != 0:
            valid = False
            try:
                int(value)
                valid = True
            except:
                pass
        self.show_invalid(not valid)
        return valid


class RealNumberEditor(EntryPropertyEditor):
    def _validate(self):
        valid = True
        value = self._get_value()
        if len(value) != 0:
            valid = False
            try:
                float(value)
                valid = True
            except:
                pass
        self.show_invalid(not valid)
        return valid


class GeometryPropertyEditor(ChoicePropertyEditor):
    RE_GEOMETRY = re.compile('\d+x\d+$')
    
    def _validate(self):
        is_valid = True
        value = self._get_value()
        if len(value) != 0:
            if not self.RE_GEOMETRY.match(value):
                is_valid = False
        self.show_invalid(not is_valid)
        return is_valid



register_editor('entry', EntryPropertyEditor)
register_editor('alphanumentry', AlphanumericEntryPropertyEditor)
register_editor('commandentry', CommandEntryPropertyEditor)
register_editor('choice', ChoicePropertyEditor)
register_editor('choice_key', ChoiceByKeyPropertyEditor)
register_editor('spinbox', SpinboxPropertyEditor)
register_editor('text', TextPropertyEditor)
register_editor('checkbutton', CheckbuttonPropertyEditor)
register_editor('naturalnumber', NaturalNumberEditor)
register_editor('integernumber', IntegerNumberEditor)
register_editor('realnumber', RealNumberEditor)
register_editor('geometryentry', GeometryPropertyEditor)



if __name__ == '__main__':
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    def make_on_change_cb(editor):
        def on_change_cb(event=None):
            print(editor.value)
            print(repr(editor.value))
        return on_change_cb

    editor = EntryPropertyEditor(root)
    editor.pack(expand=True, fill='x')
    editor.edit('MyValue')
    editor.bind('<<PropertyChanged>>', make_on_change_cb(editor))

    editor = TextPropertyEditor(root)
    editor.pack(expand=True, fill='x')
    editor.edit('MyValue 2')
    editor.bind('<<PropertyChanged>>', make_on_change_cb(editor))

    editor = SpinboxPropertyEditor(root)
    editor.pack(expand=True, fill='x')
    editor.edit('55')
    editor.parameters(from_=0, to=100, increment=2)
    editor.bind('<<PropertyChanged>>', make_on_change_cb(editor))

    editor = ChoicePropertyEditor(root)
    editor.pack(expand=True, fill='x')
    editor.edit('')
    editor.parameters(values=('A', 'B', 'C', 'D'))
    editor.bind('<<PropertyChanged>>', make_on_change_cb(editor))

    root.mainloop()
