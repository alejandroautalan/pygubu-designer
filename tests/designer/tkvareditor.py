import tkinter as tk

from pygubudesigner.properties.editors import TkVarPropertyEditor

if __name__ == "__main__":
    root = tk.Tk()
    editor = TkVarPropertyEditor(root)
    editor.grid()
    editor.edit("double:mydouble")

    def see_var(_event=None):
        print(editor.value)

    editor.bind("<<PropertyChanged>>", see_var)
    root.mainloop()
