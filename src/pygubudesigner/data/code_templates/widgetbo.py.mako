<%inherit file="base.py.mako"/>

<%block name="imports" filter="trim">
${parent.imports()}
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from ${module_fqn} import ${class_name}
</%block>

<%block name="class_definition" filter="trim">
#
# Builder definition section
#
widget_namespace = "${module_fqn}"
widget_classname = "${class_name}"
builder_namespace = "${builder_namespace}"
section_name = "Project Widgets"


class ${class_name}BO(BuilderObject):
    class_ = ${class_name}

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        return [(widget_namespace, widget_classname)]


builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, ${class_name}BO, widget_classname, ("ttk", section_name)
)
</%block>

<%block name="main"></%block>
