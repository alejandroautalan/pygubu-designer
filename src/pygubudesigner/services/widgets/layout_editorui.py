#!/usr/bin/python3
"""
New Layout Editor class

Redesign of layout editor.

UI source file: layout_editor.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrolledframe import ScrolledFrame
from pygubudesigner.properties.editors.propertyeditor import (
    LayoutManagerPropertyEditor,
)
from pygubudesigner.services.widgets.containerlayouteditor import (
    ContainerLayoutEditor,
)


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
class LayoutEditorUI(ttk.Frame):
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

        self.sframe = ScrolledFrame(self, scrolltype="both", name="sframe")
        self.sframe.configure(usemousewheel=True)
        # First object created
        on_first_object_cb(self.sframe)

        self.ftoolbar = ttk.Frame(self.sframe.innerframe, name="ftoolbar")
        self.ftoolbar.configure(height=200, padding="0 0 0 10p", width=200)
        self.expand_reset = ttk.Button(self.ftoolbar, name="expand_reset")
        self.img_layout_expand_reset = image_loader(None, "layout_expand_reset")
        self.expand_reset.configure(
            image=self.img_layout_expand_reset,
            style="Toolbutton",
            takefocus=True,
            text=_("ER"),
            width=-2,
        )
        self.expand_reset.grid(column=0, row=0)

        def expand_reset_cmd_():
            self.btn_expand_clicked("expand_reset")

        self.expand_reset.configure(command=expand_reset_cmd_)
        self.expand_all = ttk.Button(self.ftoolbar, name="expand_all")
        self.img_layout_expand_all = image_loader(None, "layout_expand_all")
        self.expand_all.configure(
            image=self.img_layout_expand_all,
            style="Toolbutton",
            takefocus=True,
            text=_("EA"),
            width=-2,
        )
        self.expand_all.grid(column=1, row=0)

        def expand_all_cmd_():
            self.btn_expand_clicked("expand_all")

        self.expand_all.configure(command=expand_all_cmd_)
        self.expand_width = ttk.Button(self.ftoolbar, name="expand_width")
        self.img_layout_expand_width = image_loader(None, "layout_expand_width")
        self.expand_width.configure(
            image=self.img_layout_expand_width,
            style="Toolbutton",
            takefocus=True,
            text=_("EW"),
            width=-2,
        )
        self.expand_width.grid(column=2, row=0)

        def expand_width_cmd_():
            self.btn_expand_clicked("expand_width")

        self.expand_width.configure(command=expand_width_cmd_)
        self.expand_height = ttk.Button(self.ftoolbar, name="expand_height")
        self.img_layout_expand__height = image_loader(
            None, "layout_expand__height"
        )
        self.expand_height.configure(
            image=self.img_layout_expand__height,
            style="Toolbutton",
            takefocus=True,
            text=_("EH"),
            width=-2,
        )
        self.expand_height.grid(column=3, row=0)

        def expand_height_cmd_():
            self.btn_expand_clicked("expand_height")

        self.expand_height.configure(command=expand_height_cmd_)
        self.ftoolbar.grid(column=0, row=0, sticky="ew")
        self.ftoolbar.columnconfigure("all", pad=2)
        self.fprop = ttk.Frame(self.sframe.innerframe, name="fprop")
        self.fprop.configure(height=100, width=200)
        label1 = ttk.Label(self.fprop)
        label1.configure(text=_("Manager:"))
        label1.grid(column=0, row=0, sticky="ew")
        self.layout_selector = LayoutManagerPropertyEditor(
            self.fprop, name="layout_selector"
        )
        self.layout_selector.grid(column=1, pady="2p", row=0, sticky="ew")
        separator1 = ttk.Separator(self.fprop)
        separator1.configure(orient="horizontal")
        separator1.grid(column=0, columnspan=2, pady="4p", row=1, sticky="ew")
        self.fprop.grid(column=0, row=1, sticky="nsew")
        self.fprop.columnconfigure("all", pad=2)
        self.cleditor = ContainerLayoutEditor(
            self.sframe.innerframe, name="cleditor"
        )
        self.cleditor.grid(column=0, pady="5p 0", row=2, sticky="ew")
        self.sframe.pack(expand=True, fill="both", side="top")
        self.configure(height="580p", padding="2p", width="280p")
        # Layout for 'fmain' skipped in custom widget template.

    def btn_expand_clicked(self, widget_id):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = LayoutEditorUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
