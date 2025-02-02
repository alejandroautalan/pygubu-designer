#!/usr/bin/python3
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
from demoappui import TooltipsDemoUI
from framescript import FrameScript
from pygubu.component.style_manager import IStyleDefinition
from pygubu.widgets.simpletooltip import Tooltipttk


#
# Customize default style for Tooltipttk
#
# Here I use the new IStyleDefinition for defining the style.
# This helps to reconfigure automatically the style if the user changes
# the theme (not shown here). At least the styles properties that
# the current theme supports to change.
#
class YellowTooltips(IStyleDefinition):
    UID = Tooltipttk.STYLE_NAME

    def setup(self, style: ttk.Style) -> None:
        style.configure(
            self.UID,
            background="yellow",
            foreground="black",
            font="Helvetica 12",
            padding="4p",
            relief=tk.SOLID,
        )


class TooltipsDemo(TooltipsDemoUI):
    def __init__(self, master=None, translator=None):
        super().__init__(master, translator)

        fslot = self.builder.get_object("fslot")
        FrameScript(fslot)

        tt_style = YellowTooltips()
        tt_style.initialize(self.mainwindow)


if __name__ == "__main__":
    app = TooltipsDemo()
    app.run()
