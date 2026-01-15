#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
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
class ProjectTreeFrameUI(ttk.Frame):
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

        self.filterentry = FilterEntry(self, name="filterentry")
        # First object created
        on_first_object_cb(self.filterentry)

        self.filterentry.pack(fill="x", pady="0 2p", side="top")
        self.filterentry.bind(
            "<<FilterEntryChanged>>", self.on_filtervalue_changed, add=""
        )
        frame3 = ttk.Frame(self)
        frame3.configure(height=200, width=200)
        self.fdisplay = ScrollbarHelper(
            frame3, scrolltype="both", name="fdisplay"
        )
        self.fdisplay.configure(usemousewheel=False)
        self.tvfilter = ttk.Treeview(self.fdisplay.container, name="tvfilter")
        self.tvfilter.configure(selectmode="extended")
        self.tvfilter_cols = ["column2", "column3", "column4", "column5"]
        self.tvfilter_dcols = ["column3", "column4", "column5"]
        self.tvfilter.configure(
            columns=self.tvfilter_cols, displaycolumns=self.tvfilter_dcols
        )
        self.tvfilter.column(
            "#0", anchor="w", stretch=False, width=200, minwidth=200
        )
        self.tvfilter.column(
            "column2", anchor="w", stretch=False, width=120, minwidth=100
        )
        self.tvfilter.column(
            "column3", anchor="w", stretch=False, width=25, minwidth=25
        )
        self.tvfilter.column(
            "column4", anchor="w", stretch=False, width=25, minwidth=25
        )
        self.tvfilter.column(
            "column5", anchor="w", stretch=False, width=20, minwidth=20
        )
        self.tvfilter.heading("#0", anchor="w", text="ID")
        self.tvfilter.heading("column2", anchor="w", text="Class")
        self.tvfilter.heading("column3", anchor="center", text="R")
        self.tvfilter.heading("column4", anchor="center", text="C")
        self.tvfilter.heading("column5", anchor="w", text=" ")
        self.fdisplay.add_child(self.tvfilter)
        self.fdisplay.place(anchor="nw", relheight=1.0, relwidth=1.0, x=0, y=0)
        self.fdata = ScrollbarHelper(frame3, scrolltype="both", name="fdata")
        self.fdata.configure(usemousewheel=False)
        self.tvdata = ttk.Treeview(self.fdata.container, name="tvdata")
        self.tvdata.configure(selectmode="extended")
        self.tvdata_cols = ["class", "row", "col", "space_trick"]
        self.tvdata_dcols = ["row", "col", "space_trick"]
        self.tvdata.configure(
            columns=self.tvdata_cols, displaycolumns=self.tvdata_dcols
        )
        self.tvdata.column(
            "#0", anchor="w", stretch=False, width=200, minwidth=200
        )
        self.tvdata.column(
            "class", anchor="w", stretch=False, width=120, minwidth=100
        )
        self.tvdata.column(
            "row", anchor="w", stretch=False, width=25, minwidth=25
        )
        self.tvdata.column(
            "col", anchor="w", stretch=False, width=25, minwidth=25
        )
        self.tvdata.column(
            "space_trick", anchor="w", stretch=False, width=20, minwidth=20
        )
        self.tvdata.heading("#0", anchor="w", text="ID")
        self.tvdata.heading("class", anchor="w", text="Class")
        self.tvdata.heading("row", anchor="center", text="R")
        self.tvdata.heading("col", anchor="center", text="C")
        self.tvdata.heading("space_trick", anchor="w", text=" ")
        self.fdata.add_child(self.tvdata)
        self.fdata.place(anchor="nw", relheight=1.0, relwidth=1.0, x=0, y=0)
        frame3.pack(expand=True, fill="both", side="top")
        self.configure(height=200, width=200)
        # Layout for 'frame1' skipped in custom widget template.

    def on_filtervalue_changed(self, event=None):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = ProjectTreeFrameUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
