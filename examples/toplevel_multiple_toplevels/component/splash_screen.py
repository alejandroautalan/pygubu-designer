#!/usr/bin/python3
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import component.splash_screenui as baseui


PROJECT_PATH = pathlib.Path(__file__).parent.parent / "appdata"


def image_loader(image_name):
    full_path = PROJECT_PATH / image_name
    print(full_path)
    return baseui.default_image_loader(full_path)


baseui.image_loader = image_loader


class SplashScreen(baseui.SplashScreenUI):
    def __init__(self, master=None):
        super().__init__(master)

    def init(self):
        self.center_window()
        self.progress_bar.start()

    def hide(self):
        self.mainwindow.withdraw()

    def update_msg(self, msg):
        self.txt_progress_var.set(msg)


if __name__ == "__main__":
    app = SplashScreen()
    app.run()
