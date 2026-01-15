#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrolledframe import ScrolledFrame
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
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
