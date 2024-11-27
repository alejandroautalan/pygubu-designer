"""
= This file is used for defining Ttk styles.

All style definitions should live in the function named:

   def setup_ttk_styles()

Use an instance of the ttk.Style class to define styles.

As this is a python module, now you can import any other
module that you need.


== In Pygubu Designer

Pygubu Designer will need to know which style definition file
you wish to use in your project.

To specify a style definition file in Pygubu Designer:
Go to: Project -> Settings -> Styles -> Browse (button)

Assuming that you have specified a style definition file,
- Use the 'style' combobox drop-down menu in Pygubu Designer
  to select a style that you have defined.
- Changes made to the chosen style definition file will be
  automatically reflected in Pygubu Designer.


The code below shows the minimal example definition file.

"""

import tkinter as tk
import tkinter.ttk as ttk


def setup_ttk_styles(master=None):
    my_font = ("helvetica", 12, "bold")

    style = ttk.Style(master)

    style.configure("primary.TButton",
                    font=my_font,
                    background="#4582EC",
                    foreground="white")
    style.configure("secondary.TButton",
                    font=my_font,
                    background="#ADB5BD",
                    foreground="white")
    style.configure("warning.TButton",
                    font=my_font,
                    background="#F0AD4E",
                    foreground="white")
    style.configure("danger.TButton",
                    font=my_font,
                    background="#D9534F",
                    foreground="white")
