import tkinter as tk
from tkinter import ttk

from pygubu.widgets.scrollbarhelper import ScrollbarHelper

from pygubudesigner.i18n import _
from pygubudesigner.services.text_editor_dialog import TextEditorDialog

from .propertyeditor import (
    PropertyEditor,
    register_editor,
)


class TextPropertyEditor(PropertyEditor):
    def _create_ui(self):
        self._sbh = ScrollbarHelper(self)
        self._sbh.grid(row=0, column=0, sticky="we")
        self._text = text = tk.Text(self._sbh.container, width=20, height=3)
        self._sbh.add_child(self._text)

        self._bnt_external = ttk.Button(self, name="_bnt_external")
        self._bnt_external.configure(
            compound="image",
            style="ExternalTextEditorButton.Toolbutton",
            text="",
        )
        self._bnt_external.grid(column=1, padx="2p 0", row=0, sticky="ns")
        self._bnt_external.configure(command=self.on_external_editor_clicked)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        text.bind("<FocusOut>", self._on_variable_changed)
        text.bind("<KeyPress>", self._on_keypress)

    def _get_value(self):
        value = self._text.get("0.0", "end-1c")
        return value

    def _set_value(self, value):
        self._text.delete("0.0", tk.END)
        self._text.insert("0.0", value)

    def on_external_editor_clicked(self):
        top = self.winfo_toplevel()
        title = _("Edit Property")
        editor = TextEditorDialog(top)
        editor.edit(self._get_value(), title)
        if editor.edit_confirmed():
            self._set_value(editor.text)
            self._on_variable_changed()


register_editor("text", TextPropertyEditor)


if __name__ == "__main__":
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    def make_on_change_cb(editor):
        def on_change_cb(event=None):
            print(editor.value)
            print(repr(editor.value))

        return on_change_cb

    test_editor = TextPropertyEditor(root)
    test_editor.pack(expand=True, fill="x")
    test_editor.edit("MyValue 2")
    test_editor.bind("<<PropertyChanged>>", make_on_change_cb(test_editor))

    root.mainloop()
