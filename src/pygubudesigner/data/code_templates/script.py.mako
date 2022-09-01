<%inherit file="base.py.mako"/>

<%block name="class_definition" filter="trim">
class ${class_name}:
%if with_i18n_support:
    def __init__(self, master=None, translator=None):
        _ = translator
        if translator is None:
            _ = lambda x: x
%else:
    def __init__(self, master=None):
%endif
        # build ui
${widget_code}
        # Main widget
        self.mainwindow = ${target_code_id}
%if set_main_menu:
        # Main menu
        _main_menu = self.create_${main_menu_id}(self.mainwindow)
        self.mainwindow.configure(menu=_main_menu)
%endif
        %if has_ttk_styles:

        self.setup_ttk_styles()
        %endif

    def run(self):
        self.mainwindow.mainloop()
    %if has_ttk_styles:

    def setup_ttk_styles(self):
        # ttk styles configuration
        self.style = style = ttk.Style()
        optiondb = style.master
${ttk_styles}
    %endif

${methods}\

${callbacks}\
</%block>
