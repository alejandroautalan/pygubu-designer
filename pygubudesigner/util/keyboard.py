# encoding: UTF-8
#
# Copyright 2012-2021 Alejandro Autalán
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


from __future__ import unicode_literals
import sys
import os
from collections import namedtuple

#
# Begin shortcut helpers
#

Keydef = namedtuple('Keydef', 'sym code')

osnt = True if os.name == 'nt' else False
oslinux = True if sys.platform == 'linux' else False


class Key:
    # Default keys used in pygubu-designer
    # TODO extend this keycode list
    # keysym, keycode (windows, linux)
    C = Keydef('c', 67 if osnt else 54)
    I = Keydef('i', 73 if osnt else 31)
    J = Keydef('j', 74 if osnt else 44)
    K = Keydef('k', 75 if osnt else 45)
    L = Keydef('l', 76 if osnt else 46)
    N = Keydef('n', 78 if osnt else 57)
    O = Keydef('o', 79 if osnt else 32)
    Q = Keydef('q', 81 if osnt else 24)
    S = Keydef('s', 83 if osnt else 39)
    V = Keydef('v', 86 if osnt else 55)
    X = Keydef('x', 88 if osnt else 53)


def key_bind(key, callback):
    '''Key Event decorator.
    Run callback if key of event match'''
    
    def key_event_manager(event):
        if osnt or oslinux:
            if event.keycode == key.code:
                callback(event)
        else:
            # TODO: keycode in mac is not unique?
            #
            # Default match with keysym
            if event.keysym == key.sym:
                callback(event)    
    
    return key_event_manager
