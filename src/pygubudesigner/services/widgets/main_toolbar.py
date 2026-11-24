#!/usr/bin/python3
"""
Main Toolbar

Main toolbar for pygubu designer.

UI source file: main_toolbar.ui
"""

import tkinter as tk

import pygubudesigner.services.widgets.main_toolbarui as baseui
from pygubudesigner import actions
from pygubudesigner.i18n import translator
from pygubudesigner.services.image_loader import iconset_loader

#
# Manual user code
#


class MainToolbar(baseui.MainToolbarUI):
    def __init__(self, master=None, **kw):
        super().__init__(
            master, translator=translator, image_loader=iconset_loader, **kw
        )
        self.app_root = self.winfo_toplevel()

    def on_item_clicked(self, widget_id):
        action_map = {
            "tbitem_new": actions.FILE_NEW,
            "tbitem_open": actions.FILE_OPEN,
            "tbitem_save": actions.FILE_SAVE,
            "tbitem_gencode": actions.PROJECT_BUILD_CODE,
        }
        if widget_id in action_map:
            self.app_root.event_generate(action_map[widget_id])


if __name__ == "__main__":
    root = tk.Tk()
    widget = MainToolbar(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
