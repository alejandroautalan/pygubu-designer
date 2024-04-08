#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.filterabletreeview import FilterableTreeview
from pygubu.widgets.scrollbarhelper import ScrollbarHelper


# Begin i18n - Setup translator in derived class file
def i18n_noop(value):
    return value


i18n_translator = i18n_noop
# End i18n

#
# Base class definition
#


class TreeComponentPaletteUI(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        _ = i18n_translator  # i18n string marker.
        frame1 = ttk.Frame(self)
        frame1.configure(height=200, padding="0 2 2 4", width=200)
        label3 = ttk.Label(frame1)
        label3.configure(
            compound="left", font="TkSmallCaptionFont", text=_("Filter:")
        )
        label3.pack(fill="both", side="left")
        entry2 = ttk.Entry(frame1)
        self.filter_text_var = tk.StringVar()
        entry2.configure(textvariable=self.filter_text_var, width=10)
        entry2.pack(expand=True, fill="both", padx="5 5", side="left")
        entry2.bind("<KeyPress>", self.on_filter_keypress, add="")
        self.btn_filter_cancel = ttk.Button(frame1, name="btn_filter_cancel")
        self.btn_filter_cancel.configure(
            style="Toolbutton", takefocus=True, width=-2
        )
        self.btn_filter_cancel.pack(fill="both", side="left")
        self.btn_filter_cancel.configure(command=self.on_filter_clear)
        separator1 = ttk.Separator(frame1)
        separator1.configure(orient="vertical")
        separator1.pack(fill="y", padx=4, side="left")
        self.fb_show_alltk = ttk.Checkbutton(frame1, name="fb_show_alltk")
        self.var_show_alltk = tk.BooleanVar()
        self.fb_show_alltk.configure(
            offvalue=False,
            onvalue=True,
            style="Toolbutton",
            text=_("tk"),
            variable=self.var_show_alltk,
            width=-2,
        )
        self.fb_show_alltk.pack(fill="both", side="left")
        self.fb_show_alltk.configure(command=self.on_show_alltk)
        frame1.pack(fill="x", side="top")
        frame3 = ttk.Frame(self)
        frame3.configure(height=200, width=200)
        scrollbarhelper3 = ScrollbarHelper(frame3, scrolltype="both")
        scrollbarhelper3.configure(usemousewheel=False)
        self.cptree = FilterableTreeview(
            scrollbarhelper3.container, name="cptree"
        )
        self.cptree.configure(style="TreeComponentPalette.Treeview")
        self.cptree_cols = []
        self.cptree_dcols = []
        self.cptree.configure(
            columns=self.cptree_cols, displaycolumns=self.cptree_dcols
        )
        self.cptree.column(
            "#0", anchor="w", stretch=True, width=200, minwidth=20
        )
        self.cptree.heading("#0", anchor="w", text=_("Components"))
        self.cptree.pack(expand=True, fill="both", side="top")
        scrollbarhelper3.add_child(self.cptree)
        scrollbarhelper3.pack(expand=True, fill="both", side="top")
        frame3.pack(expand=True, fill="both", side="top")
        self.configure(height=200, padding=2, width=200)
        self.pack(expand=True, fill="both", side="top")

    def on_filter_keypress(self, event=None):
        pass

    def on_filter_clear(self):
        pass

    def on_show_alltk(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = TreeComponentPaletteUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
