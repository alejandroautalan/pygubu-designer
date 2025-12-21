#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.dialog import Dialog
from pygubu.widgets.scrollbarhelper import ScrollbarHelper


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


class CustomMessageBoxUI:
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
            translator = i18n_translator_noop
        _ = translator  # i18n string marker.
        if image_loader is None:
            image_loader = image_loader_default
        if on_first_object_cb is None:
            on_first_object_cb = first_object_callback_noop
        # build ui
        dialog1 = Dialog(master)
        dialog1.configure(height=100, modal=True, width=200)
        mw_ = dialog1.toplevel.winfo_pixels(480)
        mh_ = dialog1.toplevel.winfo_pixels(320)
        dialog1.toplevel.minsize(mw_, mh_)
        dialog1.toplevel.resizable(True, True)
        dialog1.toplevel.title("Dialog")
        # First object created
        on_first_object_cb(dialog1)

        frame1 = ttk.Frame(dialog1.toplevel)
        frame1.configure(height=200, padding="5p", width=200)
        self.message = ttk.Label(frame1, name="message")
        self.message.configure(font="TkHeadingFont")
        self.message.pack(fill="x", pady="5p", side="top")
        scrollbarhelper1 = ScrollbarHelper(frame1, scrolltype="both")
        scrollbarhelper1.configure(usemousewheel=False)
        self.detail = tk.Text(scrollbarhelper1.container, name="detail")
        self.detail.configure(borderwidth=0, height=10, width=50)
        scrollbarhelper1.add_child(self.detail)
        scrollbarhelper1.pack(expand=True, fill="both", side="top")
        frame2 = ttk.Frame(frame1)
        frame2.configure(height=200, width=200)
        self.btn_ok = ttk.Button(frame2, name="btn_ok")
        self.btn_ok.configure(text="Ok", width=-8)
        self.btn_ok.pack(side="right")
        self.btn_ok.configure(command=self.btn_ok_clicked)
        frame2.pack(fill="x", pady="5p 0", side="top")
        frame1.pack(expand=True, fill="both", side="top")
        dialog1.bind("<<DialogClose>>", self.on_dialog_close, add="")

        # Main widget
        self.mainwindow = dialog1

    def run(self):
        self.mainwindow.mainloop()

    def btn_ok_clicked(self):
        pass

    def on_dialog_close(self, event=None):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomMessageBoxUI(root)
    app.run()
