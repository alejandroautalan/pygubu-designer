<%inherit file="base.py.mako"/>

<%block name="imports" filter="trim">
${parent.imports()}
</%block>

<%block name="class_definition" filter="trim">
def safe_i18n_translator(value):
    """i18n - Setup translator in derived class file"""
    return value


def safe_fo_callback(widget):
    """on first objec callback - Setup callback in derived class file."""
    pass


def safe_image_loader(master, image_name: str):
    """Image loader - Setup image_loader in derived class file."""
    img = None
    try:
        img = tk.PhotoImage(file=image_name, master=master)
    except tk.TclError:
        pass
    return img


#
# Base class definition
#
class ${class_name}(${widget_base_class}):
    def __init__(
        self,
        master=None,
        *,
        translator=None,
        on_first_object_cb=None,
        data_pool=None,
        image_loader=None,
        **kw
    ):
        if translator is None:
            translator = safe_i18n_translator
        _ = translator  # i18n string marker.
        if image_loader is None:
            image_loader = safe_image_loader
        if on_first_object_cb is None:
            on_first_object_cb = safe_fo_callback

        super().__init__(master, **kw)

${widget_code}

${callbacks}\
</%block>

<%block name="main">
if __name__ == "__main__":
    root = tk.Tk()
    widget = ${class_name}(root)
% if not main_widget_is_toplevel:
    widget.pack(expand=True, fill="both")
% endif
    root.mainloop()
</%block>
