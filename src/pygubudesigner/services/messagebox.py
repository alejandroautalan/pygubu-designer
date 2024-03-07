#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

import pygubudesigner.services.messageboxui as base
from pygubudesigner.preferences import DATA_DIR


base.PROJECT_PATH = DATA_DIR / "ui"
base.PROJECT_UI = base.PROJECT_PATH / "messagebox.ui"


class CustomMessageBox(base.CustomMessageBoxUI):
    def __init__(self, master=None):
        super().__init__(master)
        self.message = self.builder.get_object("lbl_message")
        self.detail = self.builder.get_object("txt_detail")

    def run(self):
        self.mainwindow.run()

    def btn_ok_clicked(self):
        self.mainwindow.emit_close_event()

    def on_dialog_close(self, event=None):
        self.mainwindow.close()
        self.mainwindow.destroy()

    def configure(self, title=None, message=None, detail=None):
        title = "Title" if title is None else title
        message = "Message" if message is None else message
        detail = "Detail" if detail is None else detail
        self.mainwindow.set_title(title)
        self.message.configure(text=message)
        self._set_detail(detail)

    def _set_detail(self, value):
        self.detail.delete("0.0", tk.END)
        state = self.detail.cget("state")
        if state == tk.DISABLED:
            self.detail.configure(state=tk.NORMAL)
            self.detail.insert("0.0", value)
            self.detail.configure(state=tk.DISABLED)
        else:
            self.detail.insert("0.0", value)


def show_error(master=None, title=None, message=None, detail=None):
    dialog = CustomMessageBox(master)
    dialog.configure(title=title, message=message, detail=detail)
    dialog.run()


if __name__ == "__main__":
    root = tk.Tk()

    def test_show():
        options = {
            "title": "Error",
            "message": "Exception error",
            "detail": "Long text detail",
        }
        show_error(root, **options)

    root.after(1000, test_show)
    root.mainloop()
