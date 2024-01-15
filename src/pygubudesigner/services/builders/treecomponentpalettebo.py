from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubudesigner.services.widgets.treecomponentpalette import (
    TreeComponentPalette,
)


class TreeComponentPaletteBO(BuilderObject):
    class_ = TreeComponentPalette


_builder_id = "treecomponentpalettebo.TreeComponentPalette"
register_widget(
    _builder_id,
    TreeComponentPaletteBO,
    "TreeComponentPalette",
    ("ttk", "Project Widgets"),
    public=False,
)
