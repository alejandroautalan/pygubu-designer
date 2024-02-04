"""
= This file is used for defining Ttk styles.

All style definitions should live in the function named:

   def setup_ttk_styles()

Use an instance of the ttk.Style class to define styles.

As this is a python module, now you can import any other
module that you need.
"""

import tkinter as tk
import tkinter.ttk as ttk


def setup_ttk_styles(master=None):
    style = ttk.Style(master)

    style.configure("LabelFieldInfo.TLabel")
    style.configure("Error.LabelFieldInfo.TLabel", foreground="red")

    style.configure(
        "Help2.LabelFieldInfo.TLabel",
        font=(None, 10, "italic"),
        foreground="blue",
    )
