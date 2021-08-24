# encoding: UTF-8
#
# Copyright 2012-2013 Alejandro Autalán
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
#
# For further info, check  http://pygubu.web.here

from __future__ import unicode_literals

import sys

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except BaseException:
    import Tkinter as tk
    import ttk

from pygubu.stockimage import *


# in-place prettyprint formatter
def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class ArrayVar(tk.Variable):
    '''A variable that works as a Tcl array variable'''

    _default = {}
    _elementvars = {}

    def __del__(self):
        self._tk.globalunsetvar(self._name)
        for elementvar in self._elementvars:
            del elementvar

    def __setitem__(self, elementname, value):
        if elementname not in self._elementvars:
            v = ArrayElementVar(varname=self._name,
                                elementname=elementname, master=self._master)
            self._elementvars[elementname] = v
        self._elementvars[elementname].set(value)

    def __getitem__(self, name):
        if name in self._elementvars:
            return self._elementvars[name].get()
        return None

    def __call__(self, elementname):
        '''Create a new StringVar as an element in the array'''
        if elementname not in self._elementvars:
            v = ArrayElementVar(varname=self._name, elementname=elementname,
                                master=self._master)
            self._elementvars[elementname] = v
        return self._elementvars[elementname]

    def set(self, dictvalue):
        # this establishes the variable as an array
        # as far as the Tcl interpreter is concerned
        self._master.eval("array set {%s} {}" % self._name)

        for (k, v) in dictvalue.items():
            self._tk.call("array", "set", self._name, k, v)

    # python 3.3 hack
    initialize = set

    def get(self):
        '''Return a dictionary that represents the Tcl array'''
        value = {}
        for (elementname, elementvar) in self._elementvars.items():
            value[elementname] = elementvar.get()
        return value


class ArrayElementVar(tk.StringVar):
    '''A StringVar that represents an element of an array'''

    def __init__(self, varname, elementname, master):
        name = "%s(%s)" % (varname, elementname)
        # python2 hack
        if sys.version_info[0] < 3:
            if isinstance(name, unicode):
                name = name.encode('UTF-8')
        tk.StringVar.__init__(self, master, None, name)


def treeview_print(tree, root=''):
    def tree_print(tree, root):
        children = tree.get_children(root)
        if root != '' and children:
            print(root)
        for item in children:
            tree_print(tree, item)
    tree_print(tree, root)


class BraceMessage:
    '''Helper class to use braces {} in log messages'''

    def __init__(self, fmt, *args, **kwargs):
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.fmt.format(*self.args, **self.kwargs)


# Helper to translate log messages with braces
trlog = BraceMessage


def virtual_event(event_name):
    '''Generate virtual event event_name'''

    def virtual_event_gen(event):
        event.widget.event_generate(event_name)

    return virtual_event_gen


def menu_iter_children(menu):
    '''Iterates all menu items (including submenus).
    Returns (menu, itemtype, index)'''
    count = menu.index(tk.END)
    if count is not None:
        cascades = []
        for i in range(0, count + 1):
            itemtype = menu.type(i)
            if itemtype == 'cascade':
                cascade = menu.nametowidget(menu.entrycget(i, 'menu'))
                cascades.append(cascade)
            yield (menu, itemtype, i)
        for m in cascades:
            for child in menu_iter_children(m):
                yield child


__style = None


def get_ttk_style():
    '''Use ttkthemes if module is installed
    '''
    global __style
    if __style is None:
        try:
            from ttkthemes.themed_style import ThemedStyle
            __style = ThemedStyle()
        except BaseException:
            __style = ttk.Style()
    return __style
