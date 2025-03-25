#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import component.main_screenui as baseui
from component.about_screen import AboutScreen
from component.config_screen import ConfigurationScreen
from component.splash_screen import SplashScreen
from component.loader import TaskExecutor, LoaderTask


class MainScreen(baseui.MainScreenUI):
    def __init__(self, master=None):
        super().__init__(master)
        self.config_screen = None
        self.about_screen = None

        #
        # Uncomment the following line if you want to test splash screen:
        # self.setup_splash()

    def on_menuitem_clicked(self, itemid):
        if itemid == "mi_quit":
            self.mainwindow.quit()
        if itemid == "mi_about":
            self.show_about()
        if itemid == "mi_config":
            self.show_config()

    def show_config(self):
        if self.config_screen is None:
            self.config_screen = ConfigurationScreen(self.mainwindow)
        self.config_screen.show()

    def show_about(self):
        if self.about_screen is None:
            self.about_screen = AboutScreen(self.mainwindow)
        self.about_screen.show()

    #
    # Splash screen management functions
    #
    def setup_splash(self):
        self.runner = TaskExecutor(self.mainwindow)
        self.loader = LoaderTask(self)
        self.splash_window: SplashScreen = None
        self.runner.start_processing()

        self.splash_show()

    def splash_show(self):
        self.mainwindow.withdraw()
        self.splash_window = SplashScreen(self.mainwindow)
        self.splash_window.init()
        self.loader.start()

    def splash_update(self, msg):
        self.runner.add(self._splash_msg, msg)

    def splash_finish(self):
        self.runner.add(self._splash_finish)

    def _splash_msg(self, msg):
        self.splash_window.update_msg(msg)

    def _splash_finish(self):
        self.splash_window.hide()
        self.center_window()
        self.mainwindow.deiconify()


if __name__ == "__main__":
    app = MainScreen()
    app.run()
