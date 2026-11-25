#!/usr/bin/python3
"""
Text editor dialog

A simple external text editor.

UI source file: text_editor_dialog.ui
"""

import tkinter as tk
import tkinter.ttk as ttk

from pygubu.widgets.dialog import Dialog
from pygubu.widgets.scrollbarhelper import ScrollbarHelper


def safe_i18n_translator(value):
    """i18n - Setup translator in derived class file"""
    return value


def safe_fo_callback(widget):
    """on first objec callback - Setup callback in derived class file."""


def safe_image_loader(master, image_name: str):
    """Image loader - Setup image_loader in derived class file."""
    img = None
    try:
        img = tk.PhotoImage(file=image_name, master=master)
    except tk.TclError:
        pass
    return img


class TextEditorDialogUI:
    def __init__(
        self,
        master=None,
        *,
        translator=None,
        on_first_object_cb=None,
        data_pool=None,
        image_loader=None,
    ):
        if translator is None:
            translator = safe_i18n_translator
        _ = translator  # i18n string marker.
        if image_loader is None:
            image_loader = safe_image_loader
        if on_first_object_cb is None:
            on_first_object_cb = safe_fo_callback
        # build ui
        self.dialog = Dialog(master)
        self.dialog.configure(modal=True)
        mw_ = self.dialog.toplevel.winfo_pixels(512)
        mh_ = self.dialog.toplevel.winfo_pixels(288)
        self.dialog.toplevel.minsize(mw_, mh_)
        # First object created
        on_first_object_cb(self.dialog)

        frame1 = ttk.Frame(self.dialog.toplevel)
        frame1.configure(height=200, padding="5p", width=200)
        scrollbarhelper1 = ScrollbarHelper(frame1, scrolltype="both")
        scrollbarhelper1.configure(usemousewheel=False)
        self.text_widget = tk.Text(scrollbarhelper1.container, name="text_widget")
        self.text_widget.configure(font="TkFixedFont", height=10, width=50)
        scrollbarhelper1.add_child(self.text_widget)
        scrollbarhelper1.pack(expand=True, fill="both", pady="0 10p", side="top")
        frame2 = ttk.Frame(frame1)
        frame2.configure(height=200, width=200)
        button1 = ttk.Button(frame2)
        button1.configure(text=_("Cancel"), width=-12)
        button1.pack(padx="0 10p", side="left")
        button1.configure(command=self.on_cancel)
        button2 = ttk.Button(frame2)
        button2.configure(text=_("Ok"), width=-12)
        button2.pack(side="left")
        button2.configure(command=self.on_save)
        frame2.pack(anchor="e", side="top")
        frame1.pack(expand=True, fill="both", side="top")
        self.dialog.bind("<<DialogClose>>", self.on_dialog_close, add="")

        # Main widget
        self.mainwindow = self.dialog

    def run(self):
        self.mainwindow.run()

    def on_cancel(self):
        pass

    def on_save(self):
        pass

    def on_dialog_close(self, event=None):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorDialogUI(root)
    app.run()
