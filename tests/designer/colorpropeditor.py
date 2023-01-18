# encoding: utf8
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
from pygubudesigner.widgets import ColorPropertyEditor

if __name__ == "__main__":
    root = tk.Tk()
    editor = ColorPropertyEditor(root)
    editor.grid()
    editor.edit("red")

    def see_var(event=None):
        print(editor.value)

    editor.bind("<<PropertyChanged>>", see_var)
    root.mainloop()
