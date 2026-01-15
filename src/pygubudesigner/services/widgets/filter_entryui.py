#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


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
class FilterEntryUI(ttk.Frame):
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

        label1 = ttk.Label(self)
        label1.configure(text="Filter:")
        # First object created
        on_first_object_cb(label1)

        label1.pack(side="left")
        self.filter_entry = ttk.Entry(self, name="filter_entry")
        self.filter_var = tk.StringVar()
        self.filter_entry.configure(textvariable=self.filter_var)
        self.filter_entry.pack(
            expand=True, fill="x", ipady="2p", padx="4p", side="left"
        )
        self.filter_entry.bind(
            "<KeyRelease>", self.on_keypress_onfilter, add=""
        )
        button1 = ttk.Button(self)
        self.img_filter_cancel = image_loader(None, "filter_cancel")
        button1.configure(
            image=self.img_filter_cancel, style="Toolbutton", text="✖", width=-2
        )
        button1.pack(side="left")
        button1.configure(command=self.on_clear_filter_clicked)
        self.configure(height=200, width=200)
        # Layout for 'frame2' skipped in custom widget template.

    def on_keypress_onfilter(self, event=None):
        pass

    def on_clear_filter_clicked(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = FilterEntryUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
