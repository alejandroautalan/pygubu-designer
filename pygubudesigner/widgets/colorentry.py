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
try:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.colorchooser
except:
    import Tkinter as tk
    import ttk
    import tkColorChooser
    tk.colorchooser = tkColorChooser

from pygubudesigner.widgets.propertyeditor import *


class ColorPropertyEditor(PropertyEditor):
    ttk_style = None  # style instance for all color instances
    def_bgcolor = ''  # default background color picked from current theme

    def _create_ui(self):
        cls = ColorPropertyEditor
        if cls.ttk_style is None:
            cls.ttk_style = ttk.Style()
            cls.def_bgcolor = cls.ttk_style.lookup('TFrame', 'background')

        self._lcolor = w = ttk.Label(self, text='', width=-1)
        w.grid(sticky='ns', padx='0 2')
        self._entry = w = ttk.Entry(self, textvariable=self._variable)
        w.grid(row=0, column=1, sticky='nsew')
        w.bind('<FocusOut>', self._on_variable_changed)
        w.bind('<KeyPress>', self._on_keypress)

        stylename = 'ColorSelectorButton.Toolbutton'
        self._button = w = ttk.Button(self, text='…', style=stylename)
        w.grid(row=0, column=2, padx="5 0")
        w.configure(command=self._on_button_click)

        self.columnconfigure(1, weight=1)

    def _on_button_click(self):
        current = self._get_value()
        txtcolor = None
        try:
            _, txtcolor = tk.colorchooser.askcolor(color=current)
            if txtcolor is not None:
                self._set_value(txtcolor)
                self._on_variable_changed(event=None)
        except tk.TclError:
            pass
        self._change_color(txtcolor)

    def _change_color(self, newcolor):
        cls = ColorPropertyEditor
        if newcolor:
            try:
                rgb = self.winfo_rgb(newcolor)
                self._lcolor.configure(
                    relief=tk.FLAT,
                    background=newcolor)
            except tk.TclError:
                pass
        else:
            self._lcolor.configure(
                relief=tk.SUNKEN,
                background=cls.def_bgcolor)

    def edit(self, value):
        PropertyEditor.edit(self, value)
        self._change_color(value)
    
    def _after_change(self):
        # update button color
        self._change_color(self._get_value())
    
    def _validate(self):
        is_valid = True
        value = self._get_value()
        if len(value) != 0:
            default = self._entry.cget('background')
            try:
                self._entry.configure(background=value)
                self._entry.configure(background=default)
            except tk.TclError:
                is_valid = False
        self.show_invalid(not is_valid)
        return is_valid


register_editor('colorentry', ColorPropertyEditor)


if __name__ == '__main__':
    root = tk.Tk()
    editor = ColorPropertyEditor(root)
    editor.grid()
    editor.edit('red')

    def see_var(event=None):
        print(editor.value)

    editor.bind('<<PropertyChanged>>', see_var)
    root.mainloop()
