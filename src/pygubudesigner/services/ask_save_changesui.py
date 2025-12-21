#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.dialog import Dialog


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


class AskSaveChangesDialogUI:
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
        self.dialog = Dialog(master)
        self.dialog.configure(height=100, modal=True, width=200)
        self.dialog.toplevel.resizable(True, True)
        self.dialog.toplevel.title("Save Changes")
        # First object created
        on_first_object_cb(self.dialog)

        fcontainer = ttk.Frame(self.dialog.toplevel)
        fcontainer.configure(height=200, padding="5p", width=200)
        frame3 = ttk.Frame(fcontainer)
        frame3.configure(height=200, padding="10p 10p 10p 20p", width=200)
        labelicon = ttk.Label(frame3)
        self.img_scd_msg = image_loader(self.dialog.toplevel, "scd_msg")
        labelicon.configure(image=self.img_scd_msg, text=_("SaveIcon"))
        labelicon.pack(fill="y", side="left")
        frame5 = ttk.Frame(frame3)
        frame5.configure(height=200, padding="10 0 0 0", width=200)
        lbl_message = ttk.Label(frame5)
        self.message_var = tk.StringVar(value=_("Message"))
        lbl_message.configure(
            font="TkDefaultFont",
            padding="0 0 0 5",
            text=_("Message"),
            textvariable=self.message_var,
        )
        lbl_message.pack(fill="x", side="top")
        lbl_detail = ttk.Label(frame5)
        self.detail_var = tk.StringVar(value=_("Detail"))
        lbl_detail.configure(
            font="TkDefaultFont", text=_("Detail"), textvariable=self.detail_var
        )
        lbl_detail.pack(fill="x", side="top")
        frame5.pack(expand=True, fill="x", side="top")
        frame3.grid(column=0, row=0, sticky="nsew")
        fbuttons = ttk.Frame(fcontainer)
        fbuttons.configure(height=200, width=200)
        btn_cancel = ttk.Button(fbuttons)
        self.img_scd_cancel = image_loader(self.dialog.toplevel, "scd_cancel")
        btn_cancel.configure(
            compound="left", image=self.img_scd_cancel, text=_("Cancel")
        )
        btn_cancel.grid(column=0, row=0, sticky="ew")
        btn_cancel.configure(command=self.on_cancel)
        btn_dontsave = ttk.Button(fbuttons)
        self.img_scd_discard = image_loader(self.dialog.toplevel, "scd_discard")
        btn_dontsave.configure(
            compound="left", image=self.img_scd_discard, text=_("Discard")
        )
        btn_dontsave.grid(column=1, padx="5p", row=0, sticky="ew")
        btn_dontsave.configure(command=self.on_discard)
        self.btn_save = ttk.Button(fbuttons, name="btn_save")
        self.img_scd_save = image_loader(self.dialog.toplevel, "scd_save")
        self.btn_save.configure(
            compound="left", image=self.img_scd_save, text=_("Save")
        )
        self.btn_save.grid(column=2, row=0, sticky="ew")
        self.btn_save.configure(command=self.on_save)
        fbuttons.grid(column=0, row=1, sticky="nsew")
        fbuttons.columnconfigure(0, weight=1)
        fbuttons.columnconfigure(1, weight=1)
        fbuttons.columnconfigure(2, weight=1)
        fcontainer.pack(expand=True, fill="both", side="top")
        fcontainer.rowconfigure(0, weight=1)
        fcontainer.columnconfigure(0, weight=1)
        self.dialog.bind("<<DialogClose>>", self.on_dialog_close, add="")

        # Main widget
        self.mainwindow = self.dialog

    def run(self):
        self.mainwindow.mainloop()

    def on_cancel(self):
        pass

    def on_discard(self):
        pass

    def on_save(self):
        pass

    def on_dialog_close(self, event=None):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = AskSaveChangesDialogUI(root)
    app.run()
