import tkinter as tk

from pygubudesigner.properties.editors import ColorPropertyEditor

if __name__ == "__main__":
    root = tk.Tk()
    editor = ColorPropertyEditor(root)
    editor.grid()
    editor.edit("red")

    def see_var(_event=None):
        print(editor.value)

    editor.bind("<<PropertyChanged>>", see_var)
    root.mainloop()
