#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import framescriptui as baseui


class FrameScript(baseui.FrameScriptUI):
    def __init__(self, master=None):
        super().__init__(master)


if __name__ == "__main__":
    root = tk.Tk()
    app = FrameScript(root)
    app.run()
