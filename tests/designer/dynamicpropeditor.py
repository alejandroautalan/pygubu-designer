# encoding: utf8
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
from pygubudesigner.widgets import DynamicPropertyEditor


if __name__ == "__main__":
    root = tk.Tk()
    modes = ("entry", "choice")
    editor = DynamicPropertyEditor(root)
    editor.parameters(modes=modes, mode="choice", values="A B C D E F G")
    editor.grid()
    editor.edit("320|240")

    def see_var(event=None):
        print(editor.value)

    editor.bind("<<PropertyChanged>>", see_var)
    root.mainloop()
