import os
import queue
import threading
import time
import tkinter as tk
import tkinter.messagebox
import pygubu  # fades


PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "demo.ui")


class LongRunningTask(threading.Thread):
    """This represents a long running task"""

    def __init__(self, app, dialog_id):
        threading.Thread.__init__(self)
        self.app = app
        self.dialog_id = dialog_id
        self.seconds = 20

    def run(self):
        """
        DO your thread safe coding here

        To update the UI,
        Send commands to the main app using self.app.task_cmd()
        """
        dialog_id = self.dialog_id
        msg = "task {0}".format(dialog_id)
        self.app.task_cmd(
            "task_start", dialog_id=dialog_id, message=msg + " starting ..."
        )

        while self.seconds > 0:
            time.sleep(1)
            self.seconds -= 1
            self.app.task_cmd(
                "task_step", dialog_id=dialog_id, message=msg + " step"
            )
        self.app.task_cmd(
            "task_stop", dialog_id=dialog_id, message=msg + " Done."
        )


class Task1Dialog(object):
    """This represents a Dialog UI that runs a long running task"""

    def __init__(self, app):
        self.app = app
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.dialog = builder.get_object("task1window", app.mainwindow)
        self.btn_start = builder.get_object("btn_start")
        self.pbar = builder.get_object("pbar")
        self.lbl_status = builder.get_object("lbl_status")
        self.builder.connect_callbacks(self)
        self.task = None

    def on_task_start(self):
        """button callback"""
        if self.task is None:
            self.task = LongRunningTask(self.app, id(self))
            self.task.start()
            self.btn_start.configure(state="disabled")
            self.lbl_status.configure(text="Running...")
            self.pbar.start(20)

    def task_stopped(self):
        """Restart the dialog to initial status"""
        self.btn_start.configure(state="normal")
        self.lbl_status.configure(text="Finished")
        self.pbar.stop()
        self.task = None

    def on_info_clicked(self):
        """Button callback"""
        tk.messagebox.showinfo(title="Task1", message="Info clicked")


class MainApp:
    """Main Application that can run multiple dialogs"""

    def __init__(self):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object("mainwindow")
        self.txtlog = builder.get_object("txtlog")
        builder.connect_callbacks(self)
        self.taskdialogs = {}

        #
        # theading stuff
        #
        self.queue = queue.Queue()
        # start queue processing.
        self.process_queue()

    def addlog(self, msg):
        msg = "{0}\n".format(msg)
        self.txtlog.insert("end", msg)
        self.mainwindow.after_idle(lambda: self.txtlog.see("end"))

    def process_queue(self):
        """Schedule queue processing."""
        self.mainwindow.after(100, self.do_process_queue)

    def do_process_queue(self):
        """Queue processing
        Process commands from thread tasks.
        """
        try:
            while 1:
                data = self.queue.get_nowait()
                cmd, args, kw = data
                self.process_command(cmd, *args, **kw)
                # Update the UI
                self.mainwindow.update()
        except queue.Empty:
            pass
        self.mainwindow.after(100, self.do_process_queue)

    def task_cmd(self, cmd, *args, **kw):
        """Put a command into queue for processing"""
        self.queue.put((cmd, args, kw))

    def process_command(self, cmd, *args, **kw):
        """PROCESS YOUR THREAD COMMANDS HERE"""
        if cmd == "task_start":
            self.addlog(kw["message"])
        elif cmd == "task_step":
            self.addlog(kw["message"])
        elif cmd == "task_stop":
            dialog_id = kw.get("dialog_id")
            self.addlog(kw["message"])
            self.taskdialogs[dialog_id].task_stopped()

    def on_start_new(self):
        """Button callback"""
        task = Task1Dialog(self)
        dialog_id = id(task)
        self.taskdialogs[dialog_id] = task
        task.dialog.run()

    def on_btnb_clicked(self):
        """Button callback"""
        tk.messagebox.showinfo(title="Myapp", message="Buton B clicked")

    def on_btna_clicked(self):
        """Button callback"""
        tk.messagebox.showinfo(title="Myapp", message="Buton A clicked")

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
