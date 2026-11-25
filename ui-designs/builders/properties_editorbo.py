#!/usr/bin/python3
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.widgets.scrolledframe import ScrolledFrame

from pygubudesigner.services.widgets.properties_editor import PropertiesEditor

#
# Builder definition section
#


class PropertiesEditorBO(BuilderObject):
    class_ = PropertiesEditor


_builder_id = "projectcustom.PropertiesEditor"
register_widget(
    _builder_id,
    PropertiesEditorBO,
    "PropertiesEditor",
    ("ttk", "Project Widgets"),
    public=False,
)
