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

import os
import sys
from collections import namedtuple
from enum import Enum

#
# Begin shortcut helpers
#

Keydef = namedtuple("Keydef", "sym code")

OS_NT = os.name == "nt"
OS_LINUX = sys.platform == "linux"


class Key(Keydef, Enum):
    # Default keys used in pygubu-designer
    # keysym, keycode (windows, linux)
    C = Keydef("c", 67 if OS_NT else 54)
    D = Keydef("d", 68 if OS_NT else 40)
    I = Keydef("i", 73 if OS_NT else 31)  # noqa: E741
    J = Keydef("j", 74 if OS_NT else 44)
    K = Keydef("k", 75 if OS_NT else 45)
    L = Keydef("l", 76 if OS_NT else 46)
    N = Keydef("n", 78 if OS_NT else 57)
    O = Keydef("o", 79 if OS_NT else 32)  # noqa: E741
    Q = Keydef("q", 81 if OS_NT else 24)
    S = Keydef("s", 83 if OS_NT else 39)
    V = Keydef("v", 86 if OS_NT else 55)
    X = Keydef("x", 88 if OS_NT else 53)


def key_bind(key, callback):
    """Key Event decorator.
    Run callback if key of event match"""

    def key_event_manager(event):
        if OS_NT or OS_LINUX:
            if event.keycode == key.code:
                callback(event)
        else:
            # Note: keycode in mac is not unique?
            #
            # Default match with keysym
            if event.keysym == key.sym:
                callback(event)

    return key_event_manager
