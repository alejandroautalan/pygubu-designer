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

class ${class_name}BO(BuilderObject):
    class_ = ${class_name}

_builder_id = "projectcustom.${class_name}"
register_widget(
    _builder_id, ${class_name}BO, "${class_name}", ("ttk", "Project Widgets")
)
</%block>

<%block name="main"></%block>
