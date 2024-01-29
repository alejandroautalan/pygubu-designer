<%inherit file="base.py.mako"/>
<%block name="project_paths" filter="trim">
</%block>

<%block name="class_definition" filter="trim">
class ${class_name}(${class_name}UI):
%if with_i18n_support and has_ttk_styles:
    def __init__(self, master=None, translator=None):
        super().__init__(master, translator, on_fist_object_cb=${ttk_styles_module}.setup_ttk_styles)
%elif with_i18n_support:
    def __init__(self, master=None, translator=None):
        super().__init__(master, translator)
%elif has_ttk_styles:
    def __init__(self, master=None, on_fist_object_cb=None):
        self.builder = builder = pygubu.Builder(
            on_first_object=${ttk_styles_module}.setup_ttk_styles)
%else:
    def __init__(self, master=None):
        super().__init__(master)
%endif

${callbacks}\
</%block>
