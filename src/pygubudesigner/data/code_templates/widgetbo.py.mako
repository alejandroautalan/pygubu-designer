<%inherit file="base.py.mako"/>

<%block name="imports" filter="trim">
${parent.imports()}
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from ${module_name} import ${class_name}
</%block>

<%block name="class_definition" filter="trim">
#
# Builder definition section
#
_widget_namespace = "${module_name}"
_widget_classname = "${class_name}"
_builder_namespace = "projectcustom"
_section_name = "Project Widgets"


class ${class_name}BO(BuilderObject):
    class_ = ${class_name}

_builder_id = f"{_builder_namespace}.{_widget_classname}"
register_widget(
    _builder_id, ${class_name}BO, _widget_classname, ("ttk", _section_name)
)
</%block>

<%block name="main"></%block>
