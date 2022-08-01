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

from pygubudesigner.widgets.propertyeditor import (
    ChoicePropertyEditor,
    register_editor,
)
from ..properties import TK_CURSORS


class CursorPropertyEditor(ChoicePropertyEditor):
    CURSORS = TK_CURSORS

    def parameters(self, **kw):
        if "values" not in kw:
            kw["values"] = ("",) + self.CURSORS
        if "state" not in kw:
            kw["state"] = "readonly"
        self._combobox.configure(**kw)


register_editor("cursorentry", CursorPropertyEditor)


if __name__ == "__main__":
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    def make_on_change_cb(editor):
        def on_change_cb(event=None):
            print(editor.value)
            print(repr(editor.value))

        return on_change_cb

    editor = CursorPropertyEditor(root)
    editor.pack(expand=True, fill="x")
    editor.edit("bogosity")
    editor.bind("<<PropertyChanged>>", make_on_change_cb(editor))

    root.mainloop()
