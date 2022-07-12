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

import tkinter as tk
import tkinter.ttk as ttk

from pygubudesigner.widgets.propertyeditor import (
    PropertyEditor,
    register_editor,
)


class PixelCoordinatePropertyEditor(PropertyEditor):
    def _create_ui(self):
        self.entry = entry = ttk.Entry(self, textvariable=self._variable)
        self.entry.pack(side="top", expand=True, fill="both")

        entry.bind("<FocusOut>", self._on_variable_changed)
        entry.bind("<KeyPress>", self._on_keypress)

    def _validate(self):
        is_valid = False
        value = self._get_value()
        vlen = len(value)
        if vlen == 0:
            is_valid = True  # Allow empty
        else:
            try:
                int(value)
                is_valid = True
            except ValueError:
                pass
        self.show_invalid(not is_valid)
        return is_valid


register_editor("pixelcoordinateentry", PixelCoordinatePropertyEditor)


if __name__ == "__main__":
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    def make_on_change_cb(editor):
        def on_change_cb(event=None):
            print("Property changed: ")
            print(editor.value)
            print(repr(editor.value))

        return on_change_cb

    editor = PixelCoordinatePropertyEditor(root)
    editor.pack(expand=True, fill="x")
    editor.edit("-10")
    editor.bind("<<PropertyChanged>>", make_on_change_cb(editor))
    root.mainloop()
