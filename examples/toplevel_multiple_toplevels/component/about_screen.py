#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import component.about_screenui as baseui


# i18n - Setup yout translator function
# baseui.i18n_translator = mytranslator


class AboutScreen(baseui.AboutScreenUI):
    def __init__(self, master=None):
        super().__init__(master)

        # Avoid window destroy when user clicks close (x) button
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.on_delete_window)

        # hidde after creation
        self.hide()

    def on_delete_window(self):
        # hide on button click
        self.hide()
        # do not destroy window, will reuse it.
        return False

    def show(self):
        self.mainwindow.deiconify()

    def hide(self):
        self.mainwindow.withdraw()


if __name__ == "__main__":
    app = AboutScreen()
    app.run()
