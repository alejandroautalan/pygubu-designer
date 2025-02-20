<%inherit file="base.py.mako"/>

<%block name="class_definition" filter="trim">
%if with_i18n_support:
#
# Begin i18n - Setup translator in derived class file
#
def i18n_noop(value): return value
i18n_translator = i18n_noop
# End i18n
%endif
%if with_image_loader:
#
# Begin image loader - Setup image_loader in derived class file
#
def default_image_loader(image_name):
    img = None
    try:
        img = tk.PhotoImage(file=image_name)
    except tk.TclError:
        pass
    return img

image_loader = default_image_loader
# End image loader
%endif

class ${class_name}:
    def __init__(self, master=None, data_pool=None):
        %if with_i18n_support:
        _ = i18n_translator  # i18n string marker.
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
%if add_window_centering_code:
    def center_init(self):
        """ If `width` and `height` are set for the main widget,
        this is the only time TK returns them. """
        self.main_w = self.mainwindow.winfo_reqwidth()
        self.main_h = self.mainwindow.winfo_reqheight()
        self.center_map = self.mainwindow.bind("<Map>", self.center)

    def center(self, event=None):
        min_w, min_h = self.mainwindow.wm_minsize()
        max_w, max_h = self.mainwindow.wm_maxsize()
        screen_w = self.mainwindow.winfo_screenwidth()
        screen_h = self.mainwindow.winfo_screenheight()
        final_w = min(screen_w, max_w,
                    max(self.main_w, min_w,
                        self.mainwindow.winfo_width(),
                        self.mainwindow.winfo_reqwidth()))
        final_h = min(screen_h, max_h,
                    max(self.main_h, min_h,
                        self.mainwindow.winfo_height(),
                        self.mainwindow.winfo_reqheight()))
        x = (screen_w // 2) - (final_w // 2)
        y = (screen_h // 2) - (final_h // 2)
        geometry = f"{final_w}x{final_h}+{x}+{y}"

        def set_geometry():
            self.mainwindow.geometry(geometry)

        self.mainwindow.after_idle(set_geometry)
        self.mainwindow.unbind("<Map>", self.center_map)

    def run(self, center=False):
        if center:
            self.center_init()
        self.mainwindow.mainloop()
%else:
    def run(self):
        self.mainwindow.mainloop()
%endif

${methods}\

${callbacks}\
</%block>
