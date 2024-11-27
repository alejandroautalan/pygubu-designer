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
    my_font = ("helvetica", 12, "bold")

    style = ttk.Style(master)

    style.configure(
        "MyColored.TButton",
        font=my_font,
        background="white",
        foreground="black",
    )

    style.configure(
        "MyColored2.TButton",
        font=my_font,
        background="#4582EC",
        foreground="blue",
    )
