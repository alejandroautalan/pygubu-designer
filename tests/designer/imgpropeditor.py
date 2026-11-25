import tkinter as tk

from pygubudesigner.properties.editors import ImagePropertyEditor

if __name__ == "__main__":
    root = tk.Tk()
    editor = ImagePropertyEditor(root)
    editor.grid()
    editor.edit("image.gif")

    def see_var(_event=None):
        print(editor.value)

    editor.bind("<<PropertyChanged>>", see_var)
    root.mainloop()
