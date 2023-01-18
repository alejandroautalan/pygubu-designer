# encoding: utf8
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
from pygubudesigner.widgets import TkVarPropertyEditor


if __name__ == "__main__":
    root = tk.Tk()
    editor = TkVarPropertyEditor(root)
    editor.grid()
    editor.edit("double:mydouble")

    def see_var(event=None):
        print(editor.value)

    editor.bind("<<PropertyChanged>>", see_var)
    root.mainloop()
