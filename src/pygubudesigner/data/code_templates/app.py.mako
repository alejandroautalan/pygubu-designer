<%inherit file="base.py.mako"/>
<%block name="project_paths" filter="trim">
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "${project_name}"
RESOURCE_PATHS = [PROJECT_PATH]
</%block>

<%block name="class_definition" filter="trim">
class ${class_name}:
    def __init__(
        self,
        master=None,
        translator=None,
        on_first_object_cb=None,
        data_pool=None
        ):
        self.builder = pygubu.Builder(
            translator=translator,
            on_first_object=on_first_object_cb,
            data_pool=data_pool
        )
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow:${widget_base_class} = self.builder.get_object("${main_widget}", master)
%if set_main_menu:
        # Main menu
        _main_menu = self.builder.get_object("${main_menu_id}", self.mainwindow)
        self.mainwindow.configure(menu=_main_menu)
%endif
    %if tkvariables:

        %for var in tkvariables:
        self.${var}:${tkvariablehints[var]} = None
        %endfor
        self.builder.import_variables(self)

    %endif
        self.builder.connect_callbacks(self)

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

${callbacks}\
</%block>
