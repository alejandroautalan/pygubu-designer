#!/usr/bin/python3
<%block name="imports" filter="trim">
${import_lines}
</%block>

<%block name="fnscript_definition" filter="trim">
def i18n_translator_noop(value):
    """i18n - Setup translator in derived class file"""
    return value


def first_object_callback_noop(widget):
    """on first objec callback - Setup callback in derived class file."""
    pass


def image_loader_default(master, image_name: str):
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
        translator = i18n_translator_noop
    _ = translator  # i18n string marker.
    if image_loader is None:
        image_loader = image_loader_default
    if on_first_object_cb is None:
        on_first_object_cb = first_object_callback_noop

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
