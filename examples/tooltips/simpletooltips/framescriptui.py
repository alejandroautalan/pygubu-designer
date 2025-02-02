#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.simpletooltip import Tooltip, Tooltipttk


#
# Begin i18n - Setup translator in derived class file
#
def i18n_noop(value):
    return value


i18n_translator = i18n_noop
# End i18n


class FrameScriptUI:
    def __init__(self, master=None, data_pool=None):
        _ = i18n_translator  # i18n string marker.
        # build ui
        frame2 = ttk.Frame(master)
        frame2.configure(height=200, padding="10p", width=200)
        labelframe1 = ttk.Labelframe(frame2)
        labelframe1.configure(
            height=200,
            padding="10p",
            text=_("Tooltip using tk.Label"),
            width=200,
        )
        button1 = ttk.Button(labelframe1)
        button1.configure(text=_("Default tooltip"), width=-15)
        tooltip1 = Tooltip(button1)
        tooltip1.configure(text=_("A simple tooltip for tkinter !"))
        button1.pack(pady="0 10p", side="top")
        button2 = ttk.Button(labelframe1)
        button2.configure(text=_("Customized tooltip"), width=-15)
        tooltip2 = Tooltip(button2)
        tooltip2.configure(
            background="#000074",
            font="{Helvetica} 16 {}",
            foreground="#d6ffff",
            text=_("A tooltip configured for button 2!"),
        )
        button2.pack(side="top")
        labelframe1.pack(padx="0 10p", side="left")
        labelframe2 = ttk.Labelframe(frame2)
        labelframe2.configure(
            height=200,
            padding="10p",
            text=_("Tooltip using ttk.Label"),
            width=200,
        )
        button3 = ttk.Button(labelframe2)
        button3.configure(text=_("Default tooltip"), width=-15)
        tooltipttk1 = Tooltipttk(button3)
        tooltipttk1.configure(text=_("A simple tooltip for tkinter  ttk !"))
        button3.pack(pady="0 10p", side="top")
        button4 = ttk.Button(labelframe2)
        button4.configure(text=_("Customized tooltip"), width=-15)
        tooltipttk2 = Tooltipttk(button4)
        tooltipttk2.configure(
            background="#d9b3d9",
            borderwidth="2p",
            font="{DejaVu Sans Mono} 14 {italic}",
            foreground="#d90000",
            relief="solid",
            text=_("A tooltip configured for button 4!"),
        )
        button4.pack(side="top")
        labelframe2.pack(side="left")
        frame2.pack(expand=True, fill="both", side="top")

        # Main widget
        self.mainwindow = frame2

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = FrameScriptUI(root)
    app.run()
