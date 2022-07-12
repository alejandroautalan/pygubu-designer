#!/usr/bin/python3
import pathlib
import time
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "timer.ui"


class TimerApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("mainwindow", master)

        self.gauge_var = None
        self.elapsed_time_var = None
        self.duration_var = None
        self.slider_var = None
        builder.import_variables(
            self,
            ["gauge_var", "elapsed_time_var", "duration_var", "slider_var"],
        )

        builder.connect_callbacks(self)

        # time
        self.timer_start = time.time()
        self.timer_duration = 5
        self.slider_var.set(self.timer_duration)
        self.on_slider_change(self.timer_duration)

        self.mainwindow.after(100, self.check_timer)

    def run(self):
        self.mainwindow.mainloop()

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
