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


class IDGenerator:
    _classnames_re = {}

    def __init__(self, capitalize_first=False, use_underscore=False):
        self.capitalize_first = capitalize_first
        self.use_underscore = use_underscore

    def generate(self, classname, index):
        name = classname.split(".")[-1]

        if self.use_underscore:
            name = f"{name}_{index}"
        else:
            name = f"{name}{index}"

        name = name.lower()

        if self.capitalize_first:
            name = name.capitalize()
        return name

    @classmethod
    def _create_re(cls, wclass):
        name = str(wclass).lower()
        if "." in name:
            name = name.split(".")[-1]
        regex = rf"(?P<name>{name})_?(?P<count>\d+)"
        cls._classnames_re[wclass] = re.compile(regex, re.UNICODE)

    @classmethod
    def is_unnamed(cls, wclass: str, identifier: str) -> bool:
        unnamed = False
        if wclass not in cls._classnames_re:
            cls._create_re(wclass)
        class_re = cls._classnames_re[wclass]
        unnamed = True if class_re.match(identifier) else False
        return unnamed


if __name__ == "__main__":
    gen = IDGenerator()
    names = [
        ("ttk.Button", "button1"),
        ("ttk.Label", "mybutton"),
        ("tk.Label", "label_1"),
        ("ttk.Label", "label_1_test"),
        ("pygubudesigner.ToplevelOrTk", "toplevel1_mytop"),
    ]
    for cls, name in names:
        unnamed = gen.is_unnamed(cls, name)
        print(name, unnamed)
