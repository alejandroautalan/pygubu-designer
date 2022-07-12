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

import re
import tkinter as tk

from pygubudesigner.widgets.propertyeditor import (
    EntryPropertyEditor,
    register_editor,
)

re_dim = "\\d+([cimp])?"
regexp = f"({re_dim})?$"
RE_DIMENSION = re.compile(regexp)
regexp = "({0})?$|{0}\\s{0}$".format(re_dim)
RE_TWO_DIMENSION = re.compile(regexp)
regexp = "({0})?$|{0}\\s{0}$|{0}\\s{0}\\s{0}\\s{0}$".format(re_dim)
RE_FOUR_DIMENSION = re.compile(regexp)


class DimensionPropertyEditor(EntryPropertyEditor):
    REGEX = RE_DIMENSION

    def __init__(self, master=None, **kw):
        EntryPropertyEditor.__init__(self, master, **kw)

    def _validate(self):
        valid = False
        value = self._get_value()
        m = self.REGEX.match(value)
        if m:
            valid = True
        self.show_invalid(not valid)
        return valid


class TwoDimensionPropertyEditor(DimensionPropertyEditor):
    REGEX = RE_TWO_DIMENSION


class FourDimensionPropertyEditor(DimensionPropertyEditor):
    REGEX = RE_FOUR_DIMENSION


register_editor("dimensionentry", DimensionPropertyEditor)
register_editor("twodimensionentry", TwoDimensionPropertyEditor)
register_editor("fourdimensionentry", FourDimensionPropertyEditor)


if __name__ == "__main__":
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    def make_on_change_cb(editor):
        def on_change_cb(event=None):
            print(editor.value)
            print(repr(editor.value))

        return on_change_cb

    editor = DimensionPropertyEditor(root)
    editor.pack(expand=True, fill="x")
    editor.edit("10m")
    editor.bind("<<PropertyChanged>>", make_on_change_cb(editor))

    editor2 = TwoDimensionPropertyEditor(root)
    editor2.pack(expand=True, fill="x")
    editor2.edit("10p 20p")
    editor2.bind("<<PropertyChanged>>", make_on_change_cb(editor2))

    editor2 = FourDimensionPropertyEditor(root)
    editor2.pack(expand=True, fill="x")
    editor2.edit("10p 20p 1m 2m")
    editor2.bind("<<PropertyChanged>>", make_on_change_cb(editor2))

    root.mainloop()
