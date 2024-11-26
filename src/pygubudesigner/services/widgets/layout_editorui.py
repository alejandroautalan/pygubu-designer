#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrolledframe import ScrolledFrame
from pygubudesigner.containerlayouteditor import ContainerLayoutEditor
from pygubudesigner.properties.editors.propertyeditor import (
    LayoutManagerPropertyEditor,
)


# Begin i18n - Setup translator in derived class file
def i18n_noop(value):
    return value


i18n_translator = i18n_noop
# End i18n

#
# Base class definition
#


class LayoutEditorUI(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        _ = i18n_translator  # i18n string marker.
        self.sframe = ScrolledFrame(self, scrolltype="both", name="sframe")
        self.sframe.configure(usemousewheel=True)
        self.ftoolbar = ttk.Frame(self.sframe.innerframe, name="ftoolbar")
        self.ftoolbar.configure(height=200, padding="0 0 0 10", width=200)
        self.expand_reset = ttk.Button(self.ftoolbar, name="expand_reset")
        self.expand_reset.configure(
            style="Toolbutton", takefocus=True, text=_("ER"), width=-2
        )
        self.expand_reset.grid(column=0, row=0)

        def expand_reset_cmd_():
            self.btn_expand_clicked("expand_reset")

        self.expand_reset.configure(command=expand_reset_cmd_)
        self.expand_all = ttk.Button(self.ftoolbar, name="expand_all")
        self.expand_all.configure(
            style="Toolbutton", takefocus=True, text=_("EA"), width=-2
        )
        self.expand_all.grid(column=1, row=0)

        def expand_all_cmd_():
            self.btn_expand_clicked("expand_all")

        self.expand_all.configure(command=expand_all_cmd_)
        self.expand_width = ttk.Button(self.ftoolbar, name="expand_width")
        self.expand_width.configure(
            style="Toolbutton", takefocus=True, text=_("EW"), width=-2
        )
        self.expand_width.grid(column=2, row=0)

        def expand_width_cmd_():
            self.btn_expand_clicked("expand_width")

        self.expand_width.configure(command=expand_width_cmd_)
        self.expand_height = ttk.Button(self.ftoolbar, name="expand_height")
        self.expand_height.configure(
            style="Toolbutton", takefocus=True, text=_("EH"), width=-2
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
        self.layout_selector.grid(column=1, pady=2, row=0, sticky="ew")
        separator1 = ttk.Separator(self.fprop)
        separator1.configure(orient="horizontal")
        separator1.grid(column=0, columnspan=2, pady=4, row=1, sticky="ew")
        self.fprop.grid(column=0, row=1, sticky="nsew")
        self.fprop.columnconfigure("all", pad=2)
        self.cleditor = ContainerLayoutEditor(
            self.sframe.innerframe, name="cleditor"
        )
        self.cleditor.grid(column=0, pady="5 0", row=2, sticky="ew")
        self.sframe.pack(expand=True, fill="both", side="top")
        self.configure(height=500, padding=2, width=300)
        self.pack(expand=True, fill="both", side="top")

    def btn_expand_clicked(self, widget_id):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = LayoutEditorUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
