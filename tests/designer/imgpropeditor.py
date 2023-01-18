# encoding: utf8
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
from pygubudesigner.widgets import ImagePropertyEditor

if __name__ == "__main__":
    root = tk.Tk()
    editor = ImagePropertyEditor(root)
    editor.grid()
    editor.edit("image.gif")

    def see_var(event=None):
        print(editor.value)

    editor.bind("<<PropertyChanged>>", see_var)
    root.mainloop()
