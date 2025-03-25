#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import component.config_screenui as baseui


# i18n - Setup yout translator function
# baseui.i18n_translator = mytranslator


class ConfigurationScreen(baseui.ConfigurationScreenUI):
    def __init__(self, master=None):
        super().__init__(master)

        # we need the parent for runing in modal mode
        self.parent = master

        # Avoid window destroy when user clicks close (x) button
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.on_delete_window)

        # hidde after creation
        self.hide()

    def on_delete_window(self):
        # hide only with close button
        # self.hide()
        # do not destroy window, will reuse it.
        return False

    def show(self):
        self.mainwindow.transient(self.parent)
        self.mainwindow.deiconify()
        self.mainwindow.wait_visibility()
        # run in modal mode
        self.mainwindow.grab_set()

    def hide(self):
        self.mainwindow.grab_release()
        self.mainwindow.withdraw()

    def on_btn_close_clicked(self):
        # process configuration

        self.hide()


if __name__ == "__main__":
    app = ConfigurationScreen()
    app.run()
