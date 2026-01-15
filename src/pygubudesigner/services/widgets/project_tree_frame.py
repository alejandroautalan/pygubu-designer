#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import pygubudesigner.services.widgets.project_tree_frameui as baseui

from typing import Callable, Optional
from pprint import pprint as pp

_filter_func = Callable[[ttk.Treeview, str, str], bool]


class BasicFilter:
    def __call__(self, tree, itemid, filter_value: str) -> bool:
        # Default filter match function.
        txt = tree.item(itemid, "text").lower()
        match_found = filter_value in txt
        return match_found


#
# Manual user code
#


class ProjectTreeFrame(baseui.ProjectTreeFrameUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        self.keypress_cbid = None
        self.filter_func = BasicFilter()
        self.filter_value = ""
        self.filtering = False

        self.tvfilter.bind(
            "<<TreeviewSelect>>", self.on_tvfilter_selection_change
        )

    # BEGIN Display methods
    def on_tvfilter_selection_change(self, event):
        if self.filtering:
            return
        sel = self.tvfilter.selection()
        if sel:
            print("setting data sel to:", sel)
            for item in sel:
                self.expand_to(self.tvdata, item)
            self.tvdata.selection_set(*sel)
            self.tvdata.see(sel[0])
        else:
            self.tvdata.selection_set("")

    # BEGIN FILTERING METHODS

    def on_filtervalue_changed(self, event=None):
        """Init filtering process with value from filter entry."""
        value = self.filterentry.getvalue()
        self._filter_apply(value)

    def _filter_apply(self, value):
        self.filtering = True
        if value == "":
            self.fdata.tkraise(self.fdisplay)
        else:
            self.filter_value = value
            data = self._filter_tree(self.tvdata, "")
            self.build_filter_display(data)
            # hide tvdata and show filtered tv
            self.fdisplay.tkraise(self.fdata)
        self.filtering = False

    def filter_by(self, value):
        return self._filter_apply(value)

    def filter_clear(self):
        self._filter_apply("")
        self.filterentry.clear()

    def _filter_tree(self, tree, item):
        """Recursive function to get matching items."""
        matching = {}
        for child in tree.get_children(item):
            match_found = self.filter_func(tree, child, self.filter_value)
            child_match = self._filter_tree(tree, child)
            if match_found or child_match:
                if child not in matching:
                    matching[child] = {}
                matching[child].update(child_match)
        return matching

    def _copy_items(
        self, stree: ttk.Treeview, dtree: ttk.Treeview, data, parent=""
    ):
        for item, children in data.items():
            item_options = stree.item(item)
            dtree.insert(parent, tk.END, iid=item, **item_options)
            self._copy_items(stree, dtree, children, item)

    def build_filter_display(self, data):
        """Iterate over the filterd items and build the
        filter display tree.
        """
        self._tree_clear(self.tvfilter)
        if data:
            self._copy_items(self.tvdata, self.tvfilter, data)
            self.expand_all(self.tvfilter)

    # BEGIN Utility functions

    def stretch_tree_column(self):
        self._stretch_column(self.tvdata)
        self._stretch_column(self.tvfilter)

    def show_item(self, item):
        self.expand_to(self.tvdata, item)

    def expand_all(self, tree: ttk.Treeview, rootitem=""):
        children = tree.get_children(rootitem)
        for item in children:
            self.expand_all(tree, item)
        if rootitem != "" and children:
            tree.item(rootitem, open=True)

    def _tree_clear(self, tree):
        items = tree.get_children()
        tree.delete(*items)

    def expand_to(self, tree: ttk.Treeview, target_item, start_item=""):
        """Search and expand tree to see itemid."""
        self._expand_to(tree, start_item, target_item)

    def _expand_to(self, tree: ttk.Treeview, rootitem, target_item):
        found = rootitem == target_item
        if not found:
            children = tree.get_children(rootitem)
            found = target_item in children
            if not found:
                for child_item in children:
                    found = self._expand_to(tree, child_item, target_item)
                    if found:
                        break
        if found and rootitem != "":
            tree.item(rootitem, open=True)
        return found

    def _stretch_column(self, tree, column="#0"):
        w = tree.winfo_width()
        stretch_col = column
        stretch_col_cwidth = 0
        cols = [stretch_col]
        cols.extend(tree.cget("displaycolumns"))
        csum = 0
        for col in cols:
            cwidth = tree.column(col, "width")
            if col == stretch_col:
                stretch_col_cwidth = cwidth
            csum += cwidth
        space_left = w - csum - 4
        if space_left > 0:
            stretch_col_cwidth += space_left
            tree.column(stretch_col, width=stretch_col_cwidth)


if __name__ == "__main__":
    root = tk.Tk()
    widget = ProjectTreeFrame(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
