#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrolledframe import ScrolledFrame
from pygubudesigner.properties.editors.propertyeditor import (
    LayoutManagerPropertyEditor,
)
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubudesigner.services.widgets.layout_editor import LayoutEditor


#
# Builder definition section
#


class LayoutEditorBO(BuilderObject):
    class_ = LayoutEditor


_builder_id = "projectcustom.LayoutEditor"
register_widget(
    _builder_id,
    LayoutEditorBO,
    "LayoutEditor",
    ("ttk", "Project Widgets"),
    public=False,
)
