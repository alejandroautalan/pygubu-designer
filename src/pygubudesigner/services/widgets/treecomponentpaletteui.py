#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.filterabletreeview import FilterableTreeview
from pygubu.widgets.scrollbarhelper import ScrollbarHelper
from pygubudesigner.services.widgets.filter_entry import FilterEntry


def i18n_translator_noop(value):
    """i18n - Setup translator in derived class file"""
    return value


def first_object_callback_noop(widget):
    """on first objec callback - Setup callback in derived class file."""
    pass


def image_loader_default(master, image_name: str):
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
class TreeComponentPaletteUI(ttk.Frame):
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
            translator = i18n_translator_noop
        _ = translator  # i18n string marker.
        if image_loader is None:
            image_loader = image_loader_default
        if on_first_object_cb is None:
            on_first_object_cb = first_object_callback_noop

        super().__init__(master, **kw)

        frame1 = ttk.Frame(self)
        frame1.configure(height=200, padding="0 2p 2p 4p", width=200)
        # First object created
        on_first_object_cb(frame1)

        self.filter_entry = FilterEntry(frame1, name="filter_entry")
        self.filter_entry.pack(side="left")
        self.filter_entry.bind(
            "<<FilterEntryChanged>>", self.on_do_filter, add=""
        )
        separator1 = ttk.Separator(frame1)
        separator1.configure(orient="vertical")
        separator1.pack(fill="y", padx="4p", side="left")
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
        scrollbarhelper3.add_child(self.cptree)
        scrollbarhelper3.pack(expand=True, fill="both", side="top")
        frame3.pack(expand=True, fill="both", side="top")
        self.configure(height=200, padding="2p", width=200)
        # Layout for 'fmain' skipped in custom widget template.

    def on_do_filter(self, event=None):
        pass

    def on_show_alltk(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = TreeComponentPaletteUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
