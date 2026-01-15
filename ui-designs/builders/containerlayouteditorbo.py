from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubudesigner.services.widgets.containerlayouteditor import (
    ContainerLayoutEditor,
)


class ContainerLayoutEditorBO(BuilderObject):
    class_ = ContainerLayoutEditor


_builder_id = "containerlayouteditorbo.ContainerLayoutEditor"
register_widget(
    _builder_id,
    ContainerLayoutEditorBO,
    "ContainerLayoutEditor",
    ("ttk", "Project Widgets"),
    public=False,
)
