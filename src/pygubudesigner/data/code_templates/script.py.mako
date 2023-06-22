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

    def center(self, event):
        """ `winfo_width` / `winfo_height` at this point return set `geometry` size. """
        x_min = max(self.main_w,
            self.mainwindow.wm_minsize()[0],
            self.mainwindow.winfo_width(),
            self.mainwindow.winfo_reqwidth())
        y_min = max(self.main_h,
            self.mainwindow.wm_minsize()[1],
            self.mainwindow.winfo_height(),
            self.mainwindow.winfo_reqheight())
        x = self.mainwindow.winfo_screenwidth() - x_min
        y = self.mainwindow.winfo_screenheight() - y_min
        self.mainwindow.geometry(f"{x_min}x{y_min}+{x // 2}+{y // 2}")
        self.mainwindow.unbind("<Map>", self.center_map)

    def run(self, center=False):
        if center:
            """ If `width` and `height` are set for the main widget,
            this is the only time TK returns them. """
            self.main_w = self.mainwindow.winfo_reqwidth()
            self.main_h = self.mainwindow.winfo_reqheight()
            self.center_map = self.mainwindow.bind("<Map>", self.center)
        self.mainwindow.mainloop()

${methods}\

${callbacks}\
</%block>
