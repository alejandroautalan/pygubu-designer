#!/usr/bin/python3
"""
Main Toolbar

Main toolbar for pygubu designer.

UI source file: main_toolbar.ui
"""

import tkinter as tk
import tkinter.ttk as ttk

from pygubu.widgets.hideableframe import HideableFrame


def safe_i18n_translator(value):
    """i18n - Setup translator in derived class file"""
    return value


def safe_fo_callback(widget):
    """on first objec callback - Setup callback in derived class file."""


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
class MainToolbarUI(HideableFrame):
    def __init__(
        self,
        master=None,
        *,
        translator=None,
        on_first_object_cb=None,
        data_pool=None,
        image_loader=None,
        **kw,
    ):
        if translator is None:
            translator = safe_i18n_translator
        _ = translator  # i18n string marker.
        if image_loader is None:
            image_loader = safe_image_loader
        if on_first_object_cb is None:
            on_first_object_cb = safe_fo_callback

        super().__init__(master, **kw)

        self.tbitem_new = ttk.Button(self, name="tbitem_new")
        self.img_tb_new = image_loader(None, "tb_new")
        self.tbitem_new.configure(
            compound="left",
            image=self.img_tb_new,
            style="Toolbutton",
            text=_("New"),
        )
        # First object created
        on_first_object_cb(self.tbitem_new)

        self.tbitem_new.pack(ipadx="2p", side="left")

        def tbitem_new_cmd_():
            self.on_item_clicked("tbitem_new")

        self.tbitem_new.configure(command=tbitem_new_cmd_)
        self.tbitem_open = ttk.Button(self, name="tbitem_open")
        self.img_tb_open = image_loader(None, "tb_open")
        self.tbitem_open.configure(
            compound="left",
            image=self.img_tb_open,
            style="Toolbutton",
            text=_("Open"),
        )
        self.tbitem_open.pack(ipadx="2p", padx="1p", side="left")

        def tbitem_open_cmd_():
            self.on_item_clicked("tbitem_open")

        self.tbitem_open.configure(command=tbitem_open_cmd_)
        self.tbitem_save = ttk.Button(self, name="tbitem_save")
        self.img_tb_save = image_loader(None, "tb_save")
        self.tbitem_save.configure(
            compound="left",
            image=self.img_tb_save,
            style="Toolbutton",
            text=_("Save"),
        )
        self.tbitem_save.pack(ipadx="2p", padx="1p 0p", side="left")

        def tbitem_save_cmd_():
            self.on_item_clicked("tbitem_save")

        self.tbitem_save.configure(command=tbitem_save_cmd_)
        separator1 = ttk.Separator(self)
        separator1.configure(orient="vertical")
        separator1.pack(fill="y", padx="4p", side="left")
        self.tbitem_gencode = ttk.Button(self, name="tbitem_gencode")
        self.img_tb_gencode = image_loader(None, "tb_gencode")
        self.tbitem_gencode.configure(
            compound="left",
            image=self.img_tb_gencode,
            style="Toolbutton",
            text=_("Build code"),
        )
        self.tbitem_gencode.pack(ipadx="2p", padx="0p 1p", side="left")

        def tbitem_gencode_cmd_():
            self.on_item_clicked("tbitem_gencode")

        self.tbitem_gencode.configure(command=tbitem_gencode_cmd_)
        self.configure(height=20, padding="2p", width=20)
        # Layout for 'fmain' skipped in custom widget template.

    def on_item_clicked(self, widget_id):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = MainToolbarUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
