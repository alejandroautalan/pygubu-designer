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
    mmain = tk.Menu(master, name="mmain")
    mmain.configure(tearoff=0)
    # First object created
    on_first_object_cb(mmain)

    mfile = tk.Menu(mmain, tearoff=0, name="mfile")
    mmain.add(tk.CASCADE, menu=mfile, label=_("File"), underline=0)
    img_mi_new = image_loader(mmain, "mi_new")

    def FILE_NEW_cmd(itemid="FILE_NEW"):
        find_callback(callbacks_bag, "on_file_menuitem_clicked")(itemid)

    mfile.add(
        "command",
        accelerator="Ctrl+N",
        command=FILE_NEW_cmd,
        compound="left",
        image=img_mi_new,
        label=_("New"),
    )
    img_mi_open = image_loader(mmain, "mi_open")

    def FILE_OPEN_cmd(itemid="FILE_OPEN"):
        find_callback(callbacks_bag, "on_file_menuitem_clicked")(itemid)

    mfile.add(
        "command",
        accelerator="Ctrl+O",
        command=FILE_OPEN_cmd,
        compound="left",
        image=img_mi_open,
        label=_("Open …"),
    )
    img_mi_menu3 = image_loader(mmain, "mi_menu3")
    mrecent = tk.Menu(mfile, tearoff=False, name="mrecent")
    mfile.add(
        tk.CASCADE,
        menu=mrecent,
        compound="left",
        image=img_mi_menu3,
        label=_("Open recent …"),
    )
    mrecent.add("separator")
    img_mi_recent_clear = image_loader(mmain, "mi_recent_clear")

    def FILE_RECENT_CLEAR_cmd(itemid="FILE_RECENT_CLEAR"):
        find_callback(callbacks_bag, "on_file_menuitem_clicked")(itemid)

    mrecent.add(
        "command",
        command=FILE_RECENT_CLEAR_cmd,
        compound="left",
        image=img_mi_recent_clear,
        label=_("Clear list"),
    )
    mfile.add("separator")
    img_mi_save = image_loader(mmain, "mi_save")

    def FILE_SAVE_cmd(itemid="FILE_SAVE"):
        find_callback(callbacks_bag, "on_file_menuitem_clicked")(itemid)

    mfile.add(
        "command",
        accelerator="Ctrl+S",
        command=FILE_SAVE_cmd,
        compound="left",
        image=img_mi_save,
        label=_("Save"),
    )
    img_mi_saveas = image_loader(mmain, "mi_saveas")

    def FILE_SAVEAS_cmd(itemid="FILE_SAVEAS"):
        find_callback(callbacks_bag, "on_file_menuitem_clicked")(itemid)

    mfile.add(
        "command",
        command=FILE_SAVEAS_cmd,
        compound="left",
        image=img_mi_saveas,
        label=_("Save as …"),
    )
    mfile.add("separator")
    img_mi_restart = image_loader(mmain, "mi_restart")

    def FILE_RESTART_cmd(itemid="FILE_RESTART"):
        find_callback(callbacks_bag, "on_file_menuitem_clicked")(itemid)

    mfile.add(
        "command",
        command=FILE_RESTART_cmd,
        compound="left",
        image=img_mi_restart,
        label=_("Restart …"),
    )
    img_mi_quit = image_loader(mmain, "mi_quit")

    def FILE_QUIT_cmd(itemid="FILE_QUIT"):
        find_callback(callbacks_bag, "on_file_menuitem_clicked")(itemid)

    mfile.add(
        "command",
        accelerator="Ctrl+Q",
        command=FILE_QUIT_cmd,
        compound="left",
        image=img_mi_quit,
        label=_("Quit …"),
    )
    medit = tk.Menu(mmain, tearoff=0, name="medit")
    mmain.add(tk.CASCADE, menu=medit, label=_("Edit"), underline=0)
    img_mi_copy = image_loader(mmain, "mi_copy")

    def TREE_ITEM_COPY_cmd(itemid="TREE_ITEM_COPY"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    medit.add(
        "command",
        accelerator="Ctrl+C",
        command=TREE_ITEM_COPY_cmd,
        compound="left",
        image=img_mi_copy,
        label=_("Copy"),
    )
    img_mi_paste = image_loader(mmain, "mi_paste")

    def TREE_ITEM_PASTE_cmd(itemid="TREE_ITEM_PASTE"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    medit.add(
        "command",
        accelerator="Ctrl+V",
        command=TREE_ITEM_PASTE_cmd,
        compound="left",
        image=img_mi_paste,
        label=_("Paste"),
    )
    img_mi_cut = image_loader(mmain, "mi_cut")

    def TREE_ITEM_CUT_cmd(itemid="TREE_ITEM_CUT"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    medit.add(
        "command",
        accelerator="Ctrl+X",
        command=TREE_ITEM_CUT_cmd,
        compound="left",
        image=img_mi_cut,
        label=_("Cut"),
    )
    img_mi_duplicate = image_loader(mmain, "mi_duplicate")

    def TREE_ITEM_DUPLICATE_cmd(itemid="TREE_ITEM_DUPLICATE"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    medit.add(
        "command",
        accelerator="Ctrl+D",
        command=TREE_ITEM_DUPLICATE_cmd,
        compound="left",
        image=img_mi_duplicate,
        label=_("Duplicate"),
    )
    medit.add("separator")
    edit_widget = tk.Menu(medit, tearoff=0, name="edit_widget")
    medit.add(
        tk.CASCADE,
        menu=edit_widget,
        compound="left",
        image=img_mi_menu3,
        label=_("Widget tree"),
    )
    img_mi_move_up = image_loader(mmain, "mi_move_up")

    def TREE_ITEM_MOVE_UP_cmd(itemid="TREE_ITEM_MOVE_UP"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    edit_widget.add(
        "command",
        accelerator="Ctrl+I",
        command=TREE_ITEM_MOVE_UP_cmd,
        compound="left",
        image=img_mi_move_up,
        label=_("Item up"),
    )
    img_mi_move_down = image_loader(mmain, "mi_move_down")

    def TREE_ITEM_MOVE_DOWN_cmd(itemid="TREE_ITEM_MOVE_DOWN"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    edit_widget.add(
        "command",
        accelerator="Ctrl+K",
        command=TREE_ITEM_MOVE_DOWN_cmd,
        compound="left",
        image=img_mi_move_down,
        label=_("Item down"),
    )
    edit_widget.add("separator")
    img_mi_delete = image_loader(mmain, "mi_delete")

    def TREE_ITEM_DELETE_cmd(itemid="TREE_ITEM_DELETE"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    edit_widget.add(
        "command",
        command=TREE_ITEM_DELETE_cmd,
        compound="left",
        image=img_mi_delete,
        label=_("Item delete"),
    )
    edit_widget_grid = tk.Menu(medit, tearoff=0, name="edit_widget_grid")
    medit.add(
        tk.CASCADE,
        menu=edit_widget_grid,
        compound="left",
        image=img_mi_menu3,
        label=_("Widget grid"),
    )

    def TREE_ITEM_GRID_UP_cmd(itemid="TREE_ITEM_GRID_UP"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    edit_widget_grid.add(
        "command",
        accelerator="Alt+I",
        command=TREE_ITEM_GRID_UP_cmd,
        compound="left",
        image=img_mi_move_up,
        label=_("Move up"),
    )

    def TREE_ITEM_GRID_DOWN_cmd(itemid="TREE_ITEM_GRID_DOWN"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    edit_widget_grid.add(
        "command",
        accelerator="Alt+K",
        command=TREE_ITEM_GRID_DOWN_cmd,
        compound="left",
        image=img_mi_move_down,
        label=_("Move down"),
    )
    img_mi_move_left = image_loader(mmain, "mi_move_left")

    def TREE_ITEM_GRID_LEFT_cmd(itemid="TREE_ITEM_GRID_LEFT"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    edit_widget_grid.add(
        "command",
        accelerator="Alt+J",
        command=TREE_ITEM_GRID_LEFT_cmd,
        compound="left",
        image=img_mi_move_left,
        label=_("Move left"),
    )
    img_mi_move_right = image_loader(mmain, "mi_move_right")

    def TREE_ITEM_GRID_RIGHT_cmd(itemid="TREE_ITEM_GRID_RIGHT"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    edit_widget_grid.add(
        "command",
        accelerator="Alt+L",
        command=TREE_ITEM_GRID_RIGHT_cmd,
        compound="left",
        image=img_mi_move_right,
        label=_("Move right"),
    )
    medit.add("separator")
    img_mi_layout_reset = image_loader(mmain, "mi_layout_reset")

    def reset_layout_cmd(itemid="reset_layout"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    medit.add(
        "command",
        command=reset_layout_cmd,
        compound="left",
        image=img_mi_layout_reset,
        label=_("Reset layout"),
    )
    medit.add("separator")
    img_mi_settings = image_loader(mmain, "mi_settings")

    def edit_preferences_cmd(itemid="edit_preferences"):
        find_callback(callbacks_bag, "on_edit_menuitem_clicked")(itemid)

    medit.add(
        "command",
        command=edit_preferences_cmd,
        compound="left",
        image=img_mi_settings,
        label=_("Preferences"),
    )
    mproject = tk.Menu(mmain, tearoff=False, name="mproject")
    mmain.add(tk.CASCADE, menu=mproject, label=_("Project"), underline=6)
    img_mi_settings_code = image_loader(mmain, "mi_settings_code")

    def project_settings_cmd(itemid="project_settings"):
        find_callback(callbacks_bag, "on_project_menuitem_clicked")(itemid)

    mproject.add(
        "command",
        command=project_settings_cmd,
        compound="left",
        image=img_mi_settings_code,
        label=_("Settings"),
    )
    mproject.add("separator")
    img_mi_code = image_loader(mmain, "mi_code")

    def project_codegen_cmd(itemid="project_codegen"):
        find_callback(callbacks_bag, "on_project_menuitem_clicked")(itemid)

    mproject.add(
        "command",
        command=project_codegen_cmd,
        compound="left",
        image=img_mi_code,
        label=_("Generate code"),
    )
    mpreview = tk.Menu(mmain, tearoff=0, name="mpreview")
    mmain.add(tk.CASCADE, menu=mpreview, label=_("Preview"), underline=0)
    img_mi_preview = image_loader(mmain, "mi_preview")

    def TREE_ITEM_PREVIEW_TOPLEVEL_cmd(itemid="TREE_ITEM_PREVIEW_TOPLEVEL"):
        find_callback(callbacks_bag, "on_previewmenu_action")(itemid)

    mpreview.add(
        "command",
        accelerator="F5",
        command=TREE_ITEM_PREVIEW_TOPLEVEL_cmd,
        compound="left",
        image=img_mi_preview,
        label=_("Preview in Toplevel"),
    )
    img_mi_preview_close = image_loader(mmain, "mi_preview_close")

    def PREVIEW_TOPLEVEL_CLOSE_ALL_cmd(itemid="PREVIEW_TOPLEVEL_CLOSE_ALL"):
        find_callback(callbacks_bag, "on_previewmenu_action")(itemid)

    mpreview.add(
        "command",
        accelerator="F6",
        command=PREVIEW_TOPLEVEL_CLOSE_ALL_cmd,
        compound="left",
        image=img_mi_preview_close,
        label=_("Close Toplevel previews"),
    )
    img_mi_theme = image_loader(mmain, "mi_theme")
    mthemes_list = tk.Menu(mpreview, tearoff=0, name="mthemes_list")
    mpreview.add(
        tk.CASCADE,
        menu=mthemes_list,
        compound="left",
        image=img_mi_theme,
        label=_("ttk theme"),
    )
    mhelp = tk.Menu(mmain, tearoff=0, name="mhelp")
    mmain.add(tk.CASCADE, menu=mhelp, label=_("Help"), underline=0)
    img_mi_wiki = image_loader(mmain, "mi_wiki")

    def help_online_cmd(itemid="help_online"):
        find_callback(callbacks_bag, "on_help_menuitem_clicked")(itemid)

    mhelp.add(
        "command",
        command=help_online_cmd,
        compound="left",
        image=img_mi_wiki,
        label=_("Pygubu wiki"),
    )
    img_mi_about = image_loader(mmain, "mi_about")

    def help_about_cmd(itemid="help_about"):
        find_callback(callbacks_bag, "on_help_menuitem_clicked")(itemid)

    mhelp.add(
        "command",
        command=help_about_cmd,
        compound="left",
        image=img_mi_about,
        label=_("About Pygubu"),
    )

    return mmain


if __name__ == "__main__":
    root = tk.Tk()
    app = create_main_menu(root)
    if isinstance(app, tk.Menu):
        root.configure(menu=app)
    root.mainloop()
