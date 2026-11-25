#!/usr/bin/python3
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.widgets.scrolledframe import ScrolledFrame

from pygubudesigner.properties.editors.propertyeditor import (
    LayoutManagerPropertyEditor,
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
