<%inherit file="base.py.mako"/>

<%block name="imports" filter="trim">
# Note: Template in development.
${parent.imports()}
</%block>

<%block name="class_definition" filter="trim">
#
# Base class definition
#
class ${class_name}Base(${widget_base_class}):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
${widget_code}

${callbacks}\


#
# Manual user code
#
from widgetbase import ${class_name}Base

class ${class_name}(${class_name}Base):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
${widget_code}

${callbacks}\

#
# Builder definition section
#
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)


class ${class_name}BO(BuilderObject):
    class_ = ${class_name}

_builder_id = "projectcustom.${class_name}"
register_widget(
    _builder_id, ${class_name}BO, "${class_name}", ("ttk", "Project Custom")
)
</%block>

<%block name="main">
if __name__ == "__main__":
    root = tk.Tk()
    widget = ${class_name}(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
</%block>
