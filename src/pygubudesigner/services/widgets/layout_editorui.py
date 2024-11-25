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
        self.ftoobar = ttk.Frame(self.sframe.innerframe, name="ftoobar")
        self.ftoobar.configure(height=200, padding="0 0 0 10", width=200)
        self.btn_center = ttk.Button(self.ftoobar, name="btn_center")
        self.btn_center.configure(
            style="Toolbutton", takefocus=True, text=_("C"), width=-2
        )
        self.btn_center.grid(column=0, row=0)

        def btn_center_cmd():
            self.btn_clicked("btn_center")

        self.btn_center.configure(command=btn_center_cmd)
        self.btn_expand = ttk.Button(self.ftoobar, name="btn_expand")
        self.btn_expand.configure(
            style="Toolbutton", takefocus=True, text=_("EA"), width=-2
        )
        self.btn_expand.grid(column=1, row=0)

        def btn_expand_cmd():
            self.btn_clicked("btn_expand")

        self.btn_expand.configure(command=btn_expand_cmd)
        self.btn_expandw = ttk.Button(self.ftoobar, name="btn_expandw")
        self.btn_expandw.configure(
            style="Toolbutton", takefocus=True, text=_("EW"), width=-2
        )
        self.btn_expandw.grid(column=2, row=0)

        def btn_expandw_cmd():
            self.btn_clicked("btn_expandw")

        self.btn_expandw.configure(command=btn_expandw_cmd)
        self.btn_expandh = ttk.Button(self.ftoobar, name="btn_expandh")
        self.btn_expandh.configure(
            style="Toolbutton", takefocus=True, text=_("EH"), width=-2
        )
        self.btn_expandh.grid(column=3, row=0)

        def btn_expandh_cmd():
            self.btn_clicked("btn_expandh")

        self.btn_expandh.configure(command=btn_expandh_cmd)
        self.ftoobar.grid(column=0, row=0, sticky="ew")
        self.ftoobar.columnconfigure("all", pad=2)
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

    def btn_clicked(self, widget_id):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = LayoutEditorUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
