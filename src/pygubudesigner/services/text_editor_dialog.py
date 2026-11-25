"""
Text editor dialog

A simple external text editor.

UI source file: text_editor_dialog.ui
"""

import tkinter as tk
from tkinter import ttk

import pygubudesigner.services.text_editor_dialogui as baseui
from pygubudesigner.i18n import translator
from pygubudesigner.services.image_loader import iconset_loader


class TextEditorDialog(baseui.TextEditorDialogUI):
    CANCEL: int = 1
    OK: int = 2

    def __init__(self, master=None):
        self.user_choice = self.CANCEL
        self.master = master
        self._textbuf: str = ""
        super().__init__(master, translator=translator, image_loader=iconset_loader)

    def on_cancel(self):
        self.user_choice = self.CANCEL
        self._textbuf = ""
        self.dialog.close()
        self.dialog.destroy()

    def on_save(self):
        self.user_choice = self.OK
        self._textbuf = self.text_widget.get("0.0", "end-1c")
        self.dialog.close()
        self.dialog.destroy()

    def on_dialog_close(self, event=None):
        # do not close window
        # force user to click cancel or acept
        pass

    def run(self, text=None, title=None) -> int:
        text = "" if text is None else text
        return self.edit(text, title)

    def edit(self, text, title=None) -> int:
        if title is None:
            title = "Text Editor"
        self.dialog.set_title(title=title)
        self.text_widget.delete("0.0", "end")
        self.text_widget.insert("0.0", text)
        self.dialog.run()
        self.text_widget.focus_set()
        self.master.wait_window(self.dialog.toplevel)
        self.dialog = None
        return self.user_choice

    @property
    def text(self) -> str:
        return self._textbuf

    def edit_confirmed(self) -> bool:
        return self.user_choice == self.OK


if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(512, 288)

    def run_test():
        editor = TextEditorDialog(root)

        text = "Edit text here."
        editor.edit(text)
        if editor.edit_confirmed():
            print("Edition confirmed.")
            print(editor.text)
        else:
            print("Edition canceled.")

    button = ttk.Button(root, text="Show dialog", command=run_test)
    button.pack(expand=True)

    root.mainloop()
