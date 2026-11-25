#!/usr/bin/python3
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.widgets.scrollbarhelper import ScrollbarHelper

from pygubudesigner.services.widgets.filter_entry import FilterEntry
from pygubudesigner.services.widgets.project_tree_frame import ProjectTreeFrame

#
# Builder definition section
#
_widget_namespace = "pygubudesigner.services.widgets.project_tree_frame"
_widget_classname = "ProjectTreeFrame"
_builder_namespace = "pygubudesigner.widget"
_section_name = "Project Widgets"


class ProjectTreeFrameBO(BuilderObject):
    class_ = ProjectTreeFrame

    def code_imports(self):
        # will return an iterable of (module, classname/function) to import
        # or None
        return [(_widget_namespace, _widget_classname)]


_builder_id = f"{_builder_namespace}.{_widget_classname}"
register_widget(
    _builder_id, ProjectTreeFrameBO, _widget_classname, ("ttk", _section_name)
)
