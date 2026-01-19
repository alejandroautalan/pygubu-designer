#!/usr/bin/python3
<%block name="module_doc" filter="trim">
"""
${project_name}

${project_doc}

UI source file: ${ui_filename}
"""
</%block>
<%block name="imports" filter="trim">
${import_lines}
</%block>

<%block name="fnscript_definition" filter="trim">
def safe_i18n_translator(value):
    """i18n - Setup translator in derived class file"""
    return value


def safe_fo_callback(widget):
    """on first objec callback - Setup callback in derived class file."""
    pass


def safe_image_loader(master, image_name: str):
    """Image loader - Setup image_loader in derived class file."""
    return tk.PhotoImage(file=image_name, master=master)


def find_callback(callbacks_bag, callback_uid):
    cb = None

    if isinstance(callbacks_bag, dict):
        if callback_uid in callbacks_bag:
            cb = callbacks_bag[callback_uid]
    elif hasattr(callbacks_bag, callback_uid):
        cb = getattr(callbacks_bag, callback_uid)
    if cb is None:

        def cb_undef(*args):
            print(f"No function defined for {callback_uid}")

        cb = cb_undef
    return cb


def ${class_name}(
    master=None,
    *,
    translator=None,
    on_first_object_cb=None,
    data_pool=None,
    image_loader=None,
    callbacks_bag=None,
    ):
    if translator is None:
        translator = safe_i18n_translator
    _ = translator  # i18n string marker.
    if image_loader is None:
        image_loader = safe_image_loader
    if on_first_object_cb is None:
        on_first_object_cb = safe_fo_callback

    #
    # Begin UI code
${widget_code}

    return ${target_code_id}
</%block>

<%block name="main" filter="trim">
if __name__ == "__main__":
% if main_widget_is_toplevel:
    app = ${class_name}()
    app.mainloop()
% else:
    root = tk.Tk()
    app = ${class_name}(root)
    if isinstance(app, tk.Menu):
        root.configure(menu=app)
    root.mainloop()
% endif
</%block>
