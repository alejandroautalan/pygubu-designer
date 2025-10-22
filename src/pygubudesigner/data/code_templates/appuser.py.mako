<%inherit file="base.py.mako"/>

<%block name="imports" filter="trim">
${parent.imports()}
%if has_ttk_styles:
import ${ttk_styles_module} # Styles definition module
%endif
</%block>


<%block name="project_paths" filter="trim">
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "${project_name}"
RESOURCE_PATHS = [PROJECT_PATH]
</%block>

<%block name="class_definition" filter="trim">
class ${class_name}(${class_name}UI):
    def __init__(self, master=None):
        super().__init__(
            master,
            project_ui=PROJECT_UI,
            resource_paths=RESOURCE_PATHS,
            translator=None, 
            on_first_object_cb=${first_object_func}
        )
        self.builder.connect_callbacks(self)

${callbacks}\
</%block>
