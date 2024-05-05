<%inherit file="base.py.mako"/>

<%block name="imports" filter="trim">
${parent.imports()}
%if has_ttk_styles:
import ${ttk_styles_module} # Styles definition module
%endif
</%block>

<%block name="project_paths" filter="trim">
</%block>

<%block name="class_definition" filter="trim">
class ${class_name}(${class_name}UI):
%if with_i18n_support and use_first_object_cb:
    def __init__(self, master=None, translator=None):
        super().__init__(master, translator, on_first_object_cb=${first_object_func})
%elif with_i18n_support:
    def __init__(self, master=None, translator=None):
        super().__init__(master, translator)
%elif use_first_object_cb:
    def __init__(self, master=None, on_first_object_cb=None):
        super().__init__(master, on_first_object_cb=${first_object_func})
%else:
    def __init__(self, master=None):
        super().__init__(master)
%endif

${callbacks}\
</%block>
