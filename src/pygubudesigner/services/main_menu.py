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


def create_main_menu(
    *,
    master=None,
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
    mainmenu = tk.Menu(master)
    mainmenu.configure(tearoff=0)
    # First object created
    on_first_object_cb(mainmenu)

    filemenu = tk.Menu(mainmenu, tearoff=0)
    mainmenu.add(tk.CASCADE, menu=filemenu, label=_("File"), underline=0)

    def FILE_NEW_cmd(itemid="FILE_NEW"):
        find_callback(callbacks_bag, "on_file_menuitem_clicked")(itemid)

    filemenu.add(
        "command", accelerator="Ctrl+N", command=FILE_NEW_cmd, label=_("New")
    )

    def FILE_OPEN_cmd(itemid="FILE_OPEN"):
        find_callback(callbacks_bag, "on_file_menuitem_clicked")(itemid)

    filemenu.add(
        "command",
        accelerator="Ctrl+O",
        command=FILE_OPEN_cmd,
        label=_("Open …"),
    )
    file_recent_menu = tk.Menu(filemenu, tearoff=False)
    filemenu.add(tk.CASCADE, menu=file_recent_menu, label=_("Open recent …"))
    file_recent_menu.add("separator")

    def FILE_RECENT_CLEAR_cmd(itemid="FILE_RECENT_CLEAR"):
        find_callback(callbacks_bag, "on_file_menuitem_clicked")(itemid)

    file_recent_menu.add(
        "command", command=FILE_RECENT_CLEAR_cmd, label=_("Clear list")
    )
    filemenu.add("separator")

    def FILE_SAVE_cmd(itemid="FILE_SAVE"):
        find_callback(callbacks_bag, "on_file_menuitem_clicked")(itemid)

    filemenu.add(
        "command", accelerator="Ctrl+S", command=FILE_SAVE_cmd, label=_("Save")
    )

    def FILE_SAVEAS_cmd(itemid="FILE_SAVEAS"):
        find_callback(callbacks_bag, "on_file_menuitem_clicked")(itemid)

    filemenu.add("command", command=FILE_SAVEAS_cmd, label=_("Save as …"))
    filemenu.add("separator")

    def FILE_QUIT_cmd(itemid="FILE_QUIT"):
        find_callback(callbacks_bag, "on_file_menuitem_clicked")(itemid)

    filemenu.add(
        "command",
        accelerator="Ctrl+Q",
        command=FILE_QUIT_cmd,
        label=_("Quit …"),
    )
    editmenu = tk.Menu(mainmenu, tearoff=0)
    mainmenu.add(tk.CASCADE, menu=editmenu, label=_("Edit"), underline=0)

    def TREE_ITEM_COPY_cmd(itemid="TREE_ITEM_COPY"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    editmenu.add(
        "command",
        accelerator="Ctrl+C",
        command=TREE_ITEM_COPY_cmd,
        label=_("Copy"),
    )

    def TREE_ITEM_PASTE_cmd(itemid="TREE_ITEM_PASTE"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    editmenu.add(
        "command",
        accelerator="Ctrl+V",
        command=TREE_ITEM_PASTE_cmd,
        label=_("Paste"),
    )

    def TREE_ITEM_CUT_cmd(itemid="TREE_ITEM_CUT"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    editmenu.add(
        "command",
        accelerator="Ctrl+X",
        command=TREE_ITEM_CUT_cmd,
        label=_("Cut"),
    )

    def TREE_ITEM_DUPLICATE_cmd(itemid="TREE_ITEM_DUPLICATE"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    editmenu.add(
        "command",
        accelerator="Ctrl+D",
        command=TREE_ITEM_DUPLICATE_cmd,
        label=_("Duplicate"),
    )
    editmenu.add("separator")
    edit_widget = tk.Menu(editmenu, tearoff=0)
    editmenu.add(tk.CASCADE, menu=edit_widget, label=_("Widget tree"))

    def TREE_ITEM_MOVE_UP_cmd(itemid="TREE_ITEM_MOVE_UP"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    edit_widget.add(
        "command",
        accelerator="Ctrl+I",
        command=TREE_ITEM_MOVE_UP_cmd,
        label=_("Item up"),
    )

    def TREE_ITEM_MOVE_DOWN_cmd(itemid="TREE_ITEM_MOVE_DOWN"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    edit_widget.add(
        "command",
        accelerator="Ctrl+K",
        command=TREE_ITEM_MOVE_DOWN_cmd,
        label=_("Item down"),
    )
    edit_widget.add("separator")

    def TREE_ITEM_DELETE_cmd(itemid="TREE_ITEM_DELETE"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    edit_widget.add(
        "command", command=TREE_ITEM_DELETE_cmd, label=_("Item delete")
    )
    edit_widget_grid = tk.Menu(editmenu, tearoff=0)
    editmenu.add(tk.CASCADE, menu=edit_widget_grid, label=_("Widget grid"))

    def TREE_ITEM_GRID_UP_cmd(itemid="TREE_ITEM_GRID_UP"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    edit_widget_grid.add(
        "command",
        accelerator="Alt+I",
        command=TREE_ITEM_GRID_UP_cmd,
        label=_("Move up"),
    )

    def TREE_ITEM_GRID_DOWN_cmd(itemid="TREE_ITEM_GRID_DOWN"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    edit_widget_grid.add(
        "command",
        accelerator="Alt+K",
        command=TREE_ITEM_GRID_DOWN_cmd,
        label=_("Move down"),
    )

    def TREE_ITEM_GRID_LEFT_cmd(itemid="TREE_ITEM_GRID_LEFT"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    edit_widget_grid.add(
        "command",
        accelerator="Alt+J",
        command=TREE_ITEM_GRID_LEFT_cmd,
        label=_("Move left"),
    )

    def TREE_ITEM_GRID_RIGHT_cmd(itemid="TREE_ITEM_GRID_RIGHT"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    edit_widget_grid.add(
        "command",
        accelerator="Alt+L",
        command=TREE_ITEM_GRID_RIGHT_cmd,
        label=_("Move right"),
    )
    editmenu.add("separator")

    def reset_layout_cmd(itemid="reset_layout"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    editmenu.add("command", command=reset_layout_cmd, label=_("Reset layout"))
    editmenu.add("separator")

    def edit_preferences_cmd(itemid="edit_preferences"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    editmenu.add(
        "command", command=edit_preferences_cmd, label=_("Preferences")
    )
    projectmenu = tk.Menu(mainmenu, tearoff=False)
    mainmenu.add(tk.CASCADE, menu=projectmenu, label=_("Project"), underline=6)

    def project_settings_cmd(itemid="project_settings"):
        find_callback(callbacks_bag, "on_project_menuitem_clicked")(itemid)

    projectmenu.add(
        "command", command=project_settings_cmd, label=_("Settings")
    )
    projectmenu.add("separator")

    def project_codegen_cmd(itemid="project_codegen"):
        find_callback(callbacks_bag, "on_project_menuitem_clicked")(itemid)

    projectmenu.add(
        "command", command=project_codegen_cmd, label=_("Generate code")
    )
    previewmenu = tk.Menu(mainmenu, tearoff=0)
    mainmenu.add(tk.CASCADE, menu=previewmenu, label=_("Preview"), underline=0)

    def TREE_ITEM_PREVIEW_TOPLEVEL_cmd(itemid="TREE_ITEM_PREVIEW_TOPLEVEL"):
        find_callback(callbacks_bag, "on_previewmenu_action")(itemid)

    previewmenu.add(
        "command",
        accelerator="F5",
        command=TREE_ITEM_PREVIEW_TOPLEVEL_cmd,
        label=_("Preview in Toplevel"),
    )

    def PREVIEW_TOPLEVEL_CLOSE_ALL_cmd(itemid="PREVIEW_TOPLEVEL_CLOSE_ALL"):
        find_callback(callbacks_bag, "on_previewmenu_action")(itemid)

    previewmenu.add(
        "command",
        accelerator="F6",
        command=PREVIEW_TOPLEVEL_CLOSE_ALL_cmd,
        label=_("Close Toplevel previews"),
    )
    preview_themes_submenu = tk.Menu(previewmenu, tearoff=0)
    previewmenu.add(
        tk.CASCADE, menu=preview_themes_submenu, label=_("ttk theme")
    )
    helpmenu = tk.Menu(mainmenu, tearoff=0)
    mainmenu.add(tk.CASCADE, menu=helpmenu, label=_("Help"), underline=0)

    def help_online_cmd(itemid="help_online"):
        find_callback(callbacks_bag, "on_help_menuitem_clicked")(itemid)

    helpmenu.add("command", command=help_online_cmd, label=_("Pygubu wiki"))

    def help_about_cmd(itemid="help_about"):
        find_callback(callbacks_bag, "on_help_menuitem_clicked")(itemid)

    helpmenu.add("command", command=help_about_cmd, label=_("About Pygubu"))

    return mainmenu


if __name__ == "__main__":
    root = tk.Tk()
    app = create_main_menu(root)
    if isinstance(app, tk.Menu):
        root.configure(menu=app)
    root.mainloop()
