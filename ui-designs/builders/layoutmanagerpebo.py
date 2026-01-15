from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubudesigner.properties.editors import LayoutManagerPropertyEditor


class LayoutManagerPropertyEditorBO(BuilderObject):
    class_ = LayoutManagerPropertyEditor


_builder_id = "layoutmanagerpebo.LayoutManagerPropertyEditor"
register_widget(
    _builder_id,
    LayoutManagerPropertyEditorBO,
    "LayoutManagerPropertyEditor",
    ("ttk", "Project Widgets"),
    public=False,
)
