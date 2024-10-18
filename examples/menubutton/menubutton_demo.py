#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from menubutton_demoui import MenubuttonDemoUI


class MenubuttonDemo(MenubuttonDemoUI):
    def __init__(self, master=None):
        super().__init__(master)
        self.option_menu2 = self.builder.get_object("option_menu2")

        # Note: as extra_menu is at toplevel, it was not created yet
        # so pass self.option_menu2 as master to create the menu.
        self.menu_extra = self.builder.get_object(
            "menu_extra", self.option_menu2
        )
        # configure menu for button
        self.option_menu2.configure(menu=self.menu_extra)


if __name__ == "__main__":
    app = MenubuttonDemo()
    app.run()
