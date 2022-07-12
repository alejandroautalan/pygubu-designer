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

from .propertyeditor import ChoicePropertyEditor, EntryPropertyEditor


class EventHandlerEditor(EntryPropertyEditor):
    RE_IDENTIFIER = re.compile("[_A-Za-z][_a-zA-Z0-9]*$")

    def is_safe_identifier(self, value):
        is_valid = True
        if keyword.iskeyword(value):
            is_valid = False
        if is_valid and not self.RE_IDENTIFIER.match(value):
            is_valid = False
        return is_valid

    def _validate(self):
        is_valid = True
        value = self._get_value()
        is_valid = self.is_safe_identifier(value) and self.is_valid_globally(
            value
        )
        self.show_invalid(not is_valid)
        return is_valid


seq_modifiers = [
    "Control",
    "Alt",
    "Shift",
    "Lock",
    "Extended",
    "Button1",
    "B1",
    "Button2",
    "B2",
    "Button3",
    "B3",
    "Button4",
    "B4",
    "Button5",
    "B5",
    "Mod1",
    "M1",
    "Command",
    "Mod2",
    "M2",
    "Option",
    "Mod3",
    "M3",
    "Mod4",
    "M4",
    "Mod5",
    "M5",
    "Meta",
    "M",
    "Double",
    "Triple",
    "Quadruple",
]
seq_types = [
    "Activate",
    "ButtonPress",
    "Button",
    "ButtonRelease",
    "Configure",
    "Deactivate",
    "Destroy",
    "Enter",
    "ExposeFocusIn",
    "FocusOut",
    "KeyPress",
    "Key",
    "KeyRelease",
    "Leave",
    "Map",
    "Motion",
    "MouseWheel",
    "Unmap",
    "Visibility",
    #    "Property",
    #    "Colormap",
    #    "CirculateRequest",
    #    "ConfigureRequest",
    #    "Create",
    #    "MapRequest",
    #    "ResizeRequest",
    #    "Gravity",
    #    "Circulate",
    #    "Reparent",
]


def build_seq_re(modifiers, types):
    modlist = "|".join(seq_modifiers)
    typelist = "|".join(seq_types)
    detail = ".+"
    re_seq = f"<(?P<mod>({modlist})-)*(?P<type>{typelist})(?P<det>-{detail})?>"
    re_vseq = "(?P<vseq><<.+>>)"
    re_key = "(?P<skey><[^< ]>)"
    re_final = f"{re_key}|{re_seq}|{re_vseq}"
    return re.compile(re_final)


def build_default_choices():
    values = []
    for t in seq_types:
        values.append(f"<{t}>")
    return tuple(values)


class SequenceEditor(ChoicePropertyEditor):
    RE_SEQUENCE = build_seq_re(seq_modifiers, seq_types)
    default_choices = build_default_choices()

    def _validate(self):
        is_valid = True
        value = self._get_value()
        if not self.RE_SEQUENCE.match(value):
            is_valid = False
        self.show_invalid(not is_valid)
        return is_valid
