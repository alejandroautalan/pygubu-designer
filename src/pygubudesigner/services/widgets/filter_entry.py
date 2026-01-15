#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import pygubudesigner.services.widgets.filter_entryui as baseui

from pygubudesigner.i18n import translator
from pygubudesigner.services.image_loader import iconset_loader

#
# Manual user code
#


class FilterEntry(baseui.FilterEntryUI):
    EVENT_ENTRY_CHANGED = "<<FilterEntryChanged>>"
    KEY_PRESS_CB_MILISECONDS = 500

    def __init__(self, master=None, **kw):
        super().__init__(master, image_loader=iconset_loader, **kw)

        self.prev_value = ""
        self.keypress_cbid = None

    def evaluate_change(self):
        value = self.filter_var.get()
        if self.prev_value != value:
            self.event_generate(self.EVENT_ENTRY_CHANGED)
            self.prev_value = value

    def on_keypress_onfilter(self, event=None):
        if self.keypress_cbid is not None:
            self.after_cancel(self.keypress_cbid)
        self.keypress_cbid = self.after(
            self.KEY_PRESS_CB_MILISECONDS, self.on_keypress_onfilter_execute
        )

    def on_keypress_onfilter_execute(self):
        self.evaluate_change()
        self.keypress_cbid = None

    def on_clear_filter_clicked(self):
        self.filter_var.set("")
        self.evaluate_change()

    def setvalue(self, value: str, notify_change=True):
        if notify_change:
            self.filter_var.set("")
            self.evaluate_change()
        else:
            self.prev_value = ""
            self.filter_var.set("")

    def getvalue(self) -> str:
        return self.filter_var.get()

    def clear(self, notify_change=False):
        self.setvalue("", notify_change)


if __name__ == "__main__":
    root = tk.Tk()
    widget = FilterEntry(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
