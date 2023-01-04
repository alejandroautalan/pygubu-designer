#!/usr/bin/python3
import pathlib
import random
import pygubu
from string import Template

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demo1.ui"


events = [
    Template("Hull impact at ($x, $y, $z)"),
    Template("Door opened at sector $sector"),
    Template("Door closed at sector $sector"),
    Template("Object detected at ($x, $y, $z)"),
    Template("New message from channel $channel"),
]

times = [500, 1000, 1500, 2000, 3000, 5000]


class Demo1App:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)

        self.txt_log = builder.get_object("txt_log")
        self.mainwindow.after(400, self.random_log)

    def log_msg(self, msg: str):
        txt = self.txt_log
        txt.config(state="normal")
        txt.insert("end", msg + "\n")
        txt.config(state="disabled")
        # Scroll to see the last message.
        txt.see("end")

    def random_log(self):
        params = {
            "x": random.randint(0, 900),
            "y": random.randint(0, 900),
            "z": random.randint(0, 900),
            "sector": random.randint(0, 500),
            "channel": random.randint(1, 12),
        }
        msg: Template = random.choice(events)
        self.log_msg(msg.safe_substitute(params))
        time = random.choice(times)
        self.mainwindow.after(time, self.random_log)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = Demo1App()
    app.run()
