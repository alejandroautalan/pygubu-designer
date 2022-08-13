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
import tkinter.ttk as ttk

from pygubudesigner.widgets.propertyeditor import (
    ChoicePropertyEditor,
    register_editor,
)


class TtkStylePropertyEditor(ChoicePropertyEditor):
    RE_TTKSTYLECLASS = re.compile(
        "(?i)$|[_A-Za-z](\\.[_a-zA-Z0-9]+|[_a-zA-Z0-9]*)*$"
    )
    STYLES = []
    STYLES_FILTER_HINTS = None

    def _validate(self):
        valid = False
        value = self._get_value()
        m = self.RE_TTKSTYLECLASS.match(value)
        if m:
            valid = True
        self.show_invalid(not valid)
        return valid

    def parameters(self, **kw):
        kw["values"] = self._create_style_options(kw.get("values"))
        self._combobox.configure(**kw)

    @classmethod
    def set_filter_hints(cls, hints):
        cls.STYLES_FILTER_HINTS = hints

    @classmethod
    def set_global_style_list(cls, style_list):
        cls.STYLES = style_list

    def _create_style_options(self, styles):
        new_list = [] if styles is None else list(styles)
        if self.STYLES_FILTER_HINTS:
            for s in self.STYLES:
                for hint in self.STYLES_FILTER_HINTS:
                    if s.endswith(hint):
                        new_list.append(s)
                        break
        return new_list


register_editor("ttkstylechoice", TtkStylePropertyEditor)


if __name__ == "__main__":
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    def make_on_change_cb(editor):
        def on_change_cb(event=None):
            print(editor.value)
            print(repr(editor.value))

        return on_change_cb

    editor = TtkStylePropertyEditor(root)
    editor.pack(expand=True, fill="x")
    editor.edit("mystyle.TButton")
    editor.bind("<<PropertyChanged>>", make_on_change_cb(editor))

    root.mainloop()
