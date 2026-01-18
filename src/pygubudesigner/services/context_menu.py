#!/usr/bin/python3
import tkinter as tk


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


def create_context_menu(
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
    mcontext = tk.Menu(master, name="mcontext")
    mcontext.configure(tearoff=False)
    # First object created
    on_first_object_cb(mcontext)

    mcontext.add(
        "command",
        command=find_callback(
            callbacks_bag, "on_context_menu_go_to_parent_clicked"
        ),
        label=_("Go to parent"),
    )
    mcontext.add("separator")
    mcontext.add(
        "command",
        command=find_callback(callbacks_bag, "on_context_menu_update_preview"),
        label=_("Update preview"),
    )
    mcontext.add("separator")
    mcontext.add(
        "command",
        command=find_callback(callbacks_bag, "on_context_menu_copy_clicked"),
        label=_("Copy"),
    )
    mcontext.add(
        "command",
        command=find_callback(callbacks_bag, "on_context_menu_paste_clicked"),
        label=_("Paste"),
    )
    mcontext.add(
        "command",
        command=find_callback(callbacks_bag, "on_context_menu_cut_clicked"),
        label=_("Cut"),
    )
    mcontext.add(
        "command",
        command=find_callback(callbacks_bag, "on_context_menu_delete_clicked"),
        label=_("Delete"),
    )
    mcontext.add("separator")
    mcontext.add(
        "command",
        command=find_callback(
            callbacks_bag, "on_context_menu_duplicate_clicked"
        ),
        label=_("Duplicate"),
    )

    return mcontext


if __name__ == "__main__":
    root = tk.Tk()
    app = create_context_menu(root)
    if isinstance(app, tk.Menu):
        root.configure(menu=app)
    root.mainloop()
