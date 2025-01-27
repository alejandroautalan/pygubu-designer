#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrolledframe import ScrolledFrame


#
# Begin i18n - Setup translator in derived class file
#
def i18n_noop(value):
    return value


i18n_translator = i18n_noop
# End i18n

#
# Base class definition
#


class PropertiesEditorUI(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        _ = i18n_translator  # i18n string marker.
        scrolledframe1 = ScrolledFrame(self, scrolltype="both")
        scrolledframe1.configure(usemousewheel=True)
        self.fprop = ttk.Frame(scrolledframe1.innerframe, name="fprop")
        self.fprop.configure(height=200, width=200)
        self.fprop.pack(fill="x", side="top")
        scrolledframe1.pack(expand=True, fill="both", side="top")
        self.configure(height="580p", padding="2p", width="280p")
        self.pack(expand=True, fill="both", side="top")


if __name__ == "__main__":
    root = tk.Tk()
    widget = PropertiesEditorUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
