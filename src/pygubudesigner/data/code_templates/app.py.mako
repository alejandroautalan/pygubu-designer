<%inherit file="base.py.mako"/>
<%block name="project_paths" filter="trim">
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "${project_name}"
</%block>

<%block name="class_definition" filter="trim">
class ${class_name}:
%if with_i18n_support:
    def __init__(self, master=None, translator=None):
        self.builder = builder = pygubu.Builder(translator)
%else:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
%endif
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("${main_widget}", master)
%if set_main_menu:
        # Main menu
        _main_menu = builder.get_object("${main_menu_id}", self.mainwindow)
        self.mainwindow.configure(menu=_main_menu)
%endif
        %if tkvariables:

          %for var in tkvariables:
        self.${var} = None
          %endfor
        builder.import_variables(self, ${tkvariables})

        %endif
        %if has_ttk_styles:

        self.setup_ttk_styles()

        %endif
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()
    %if has_ttk_styles:

    def setup_ttk_styles(self):
        # ttk styles configuration
        self.style = style = ttk.Style()
        optiondb = style.master
${ttk_styles}
    %endif

${callbacks}\
</%block>
