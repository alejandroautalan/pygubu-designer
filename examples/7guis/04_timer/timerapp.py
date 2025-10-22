#!/usr/bin/python3
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import time
import pygubu
from timerappui import TimerAppUI

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "timer.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class TimerApp(TimerAppUI):
    def __init__(self, master=None):
        super().__init__(
            master,
            project_ui=PROJECT_UI,
            resource_paths=RESOURCE_PATHS,
            translator=None,
            on_first_object_cb=None,
        )
        self.builder.connect_callbacks(self)

        # time
        self.timer_start = time.time()
        self.timer_duration = 5
        self.slider_var.set(self.timer_duration)
        self.on_slider_change(self.timer_duration)

        self.mainwindow.after(100, self.check_timer)

    def check_timer(self):
        elapsed = time.time() - self.timer_start
        if elapsed < self.timer_duration:
            percent = elapsed * 100 / self.timer_duration
            self.gauge_var.set(percent)
            self.elapsed_time_var.set(f"{elapsed:.0f} s")
        if elapsed > self.timer_duration:
            self.gauge_var.set(100)
        self.mainwindow.after(100, self.check_timer)

    def on_slider_change(self, scale_value):
        value = int(float(scale_value))
        self.timer_duration = value
        label = f"Duration: {value} s"
        self.duration_var.set(label)

    def on_reset_clicked(self):
        self.timer_start = time.time()


if __name__ == "__main__":
    app = TimerApp()
    app.run()
