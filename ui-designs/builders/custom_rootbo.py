import os
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.i18n import _
from pygubu.plugins.tk.tkstdwidgets import TKToplevel as TKToplevelBO
from pygubu.plugins.tk.tkstdwidgets import TKRootBO
from pygubudesigner.services.widgets.custom_root import CustomRoot


_group_name = "Project Widgets"
_namespace = "pygubudesigner.services.widgets.custom_root"
_classname = "CustomRoot"


class CustomRootBO(TKRootBO):
    class_ = CustomRoot

    #
    # Code generation methods
    #

    def code_imports(self):
        # will return an iterable of (module, classname/function) to import
        # or None
        return [(_namespace, _classname)]


_builder_id = f"{_namespace}.{_classname}"
register_widget(_builder_id, CustomRootBO, _classname, ("ttk", _group_name))
_custom_root_buid = _builder_id


if "PYGUBU_DESIGNER_RUNNING" in os.environ:
    from typing import Optional
    from pygubu.api.v1 import BuilderLoaderPlugin
    from pygubu.api.v1 import IDesignerPlugin
    from pygubu.component.plugin_manager import PluginManager
    from pygubu.plugins.pygubu.designer.toplevelframe import (
        ToplevelFramePreviewBO,
    )

    class CustomRootPlugin(BuilderLoaderPlugin, IDesignerPlugin):
        _module = "custom_rootbo"

        #
        # IPluginBase interface methodsttk.Frame
        #
        def do_activate(self) -> bool:
            return True

        def get_designer_plugin(self) -> Optional[IDesignerPlugin]:
            return self

        #
        # IBuilderLoaderPlugin interface methods
        #
        def get_module_for(self, identifier: str) -> str:
            return self._module

        def get_all_modules(self):
            return (self._module,)

        def can_load(self, identifier: str) -> bool:
            return identifier.startswith(_namespace)

        #
        # IDesignerPlugin interface methods
        #
        def get_preview_builder(self, builder_uid: str):
            if builder_uid == _custom_root_buid:
                return ToplevelFramePreviewBO
            return None

    register_custom_property(_custom_root_buid, "minsize", "whentry")

    plugin = CustomRootPlugin()
    PluginManager.plugins.append(plugin)
    PluginManager.designer_plugins.append(plugin)
