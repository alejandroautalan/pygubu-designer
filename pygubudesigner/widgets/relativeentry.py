from __future__ import unicode_literals
import re
try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

from .propertyeditor import PropertyEditor, register_editor


class RelativeEntryPropertyEditor(PropertyEditor):
    def _create_ui(self):
        self._scheduled = None
        self.scalevar = tk.DoubleVar()
        self.entry = entry = ttk.Entry(self, textvariable=self._variable)
        self.entry.configure(width='4')
        self.entry.pack(side='left')
        
        self.scale = ttk.Scale(self, variable=self.scalevar,
                               command=self.on_scale_changed)
        self.scale.configure(from_='0', orient='horizontal', to='1', value='0')
        self.scale.pack(expand='true', fill='both', side='left')
        
        entry.bind('<FocusOut>', self._on_variable_changed)
        entry.bind('<KeyPress-Return>', self._on_variable_changed)
        entry.bind('<KeyPress-KP_Enter>', self._on_variable_changed)
    
    def _validate(self):
        is_valid = False
        value = self._get_value()
        vlen = len(value)
        if vlen == 0:
            is_valid = True  # Allow empty string
        else:
            try:
                float(value)
                is_valid = True
            except ValueError:
                pass
        self.show_invalid(not is_valid)
        return is_valid
    
    def on_scale_changed(self, value):
        value = round(self.scalevar.get(), 2)
        self._variable.set(value)
        if self._scheduled is None:
            self._scheduled = self.scale.after(1000, self._update_after)
    
    def _update_after(self):
        self._on_variable_changed()
        self._scheduled = None
    
    def _set_value(self, value):
        """Save value on storage"""
        self._variable.set(value)
        # if empty value, set scale value to zero
        scale_value = 0 if len(value) == 0 else value
        self.scalevar.set(scale_value)
    
    def _after_change(self):
        self.scalevar.set(self._variable.get())


register_editor('relativeentry', RelativeEntryPropertyEditor)


if __name__ == '__main__':
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    def make_on_change_cb(editor):
        def on_change_cb(event=None):
            print('Property changed: ')
            print(editor.value)
            print(repr(editor.value))
        return on_change_cb

    editor = RelativeEntryPropertyEditor(root)
    editor.pack(expand=True, fill='x')
    editor.edit('0.5')
    editor.bind('<<PropertyChanged>>', make_on_change_cb(editor))
    root.mainloop()
