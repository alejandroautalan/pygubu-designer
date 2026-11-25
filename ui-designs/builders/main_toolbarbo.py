#!/usr/bin/python3
"""
Main Toolbar

Main toolbar for pygubu designer.

UI source file: main_toolbar.ui
"""

from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.widgets.simpletooltip import Tooltipttk

from pygubudesigner.services.widgets.main_toolbar import MainToolbar

#
# Builder definition section
#
widget_namespace = "pygubudesigner.services.widgets.main_toolbar"
widget_classname = "MainToolbar"
builder_namespace = "pygubudesigner.widget"
section_name = "Project Widgets"


class MainToolbarBO(BuilderObject):
    class_ = MainToolbar

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        return [(widget_namespace, widget_classname)]


builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(builder_id, MainToolbarBO, widget_classname, ("ttk", section_name))
