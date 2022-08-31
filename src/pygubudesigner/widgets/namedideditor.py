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

import keyword
import re
import tkinter.ttk as ttk
from .propertyeditor import PropertyEditor, register_editor


class NamedIDPropertyEditor(PropertyEditor):
    RE_IDENTIFIER = re.compile("[_A-Za-z][_a-zA-Z0-9]*$", re.UNICODE)

    def _create_ui(self):
        self._placeholder = ""
        self._entry = entry = ttk.Entry(self, textvariable=self._variable)
        entry.grid(sticky="we")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        entry.bind("<FocusIn>", self._on_focusin)
        entry.bind("<FocusOut>", self._on_focusout)
        entry.bind("<KeyPress>", self._on_keypress)

    def _validate(self):
        is_valid = True
        value = self._get_value()
        if len(value) > 0:
            if keyword.iskeyword(value):
                is_valid = False
            if is_valid and not self.RE_IDENTIFIER.match(value):
                is_valid = False
            # Check if new id is unique
            if is_valid and value != self._initvalue:
                is_valid = self.is_valid_globally(value)
        self.show_invalid(not is_valid)
        return is_valid

    def parameters(self, **kw):
        self._placeholder = kw.get("placeholder", "")

    def _get_value(self):
        value = self._variable.get()
        if not value:
            value = self._placeholder
        print(f"getting value: {value}")
        return value

    def _set_value(self, value):
        """Save value on storage"""
        if not value:
            value = self._placeholder
        print(f"setting value: {value}")
        self._variable.set(value)

    def _on_focusin(self, event):
        if self._variable.get() == self._placeholder:
            # self._entry.delete('0', 'end')
            self._variable.set("")

    def _on_focusout(self, event):
        if not self._variable.get():
            self._variable.set(self._placeholder)
        self._on_variable_changed()


register_editor("namedid", NamedIDPropertyEditor)
