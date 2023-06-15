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

    def run(self, center=False):
        if center:
            x_min = self.mainwindow.wm_minsize()[0]
            y_min = self.mainwindow.wm_minsize()[1]
            if x_min == 1 or y_min == 1:
                geom = self.builder.objects[list(self.builder.objects)[0]]
                geom = geom.wmeta.properties["geometry"].split("x")
                x_min = int(geom[0])
                y_min = int(geom[1])
            x = self.mainwindow.winfo_screenwidth() - x_min
            y = self.mainwindow.winfo_screenheight() - y_min
            self.mainwindow.geometry(f"+{x // 2}+{y // 2}")
        self.mainwindow.mainloop()

${methods}\

${callbacks}\
</%block>
