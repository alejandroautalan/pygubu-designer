import threading
import queue
import time


class TaskExecutor:
    """A callback executor using the tkinter loop."""

    def __init__(self, master=None, delay_ms=200):
        self.delay = delay_ms
        self.tasks = queue.Queue()
        self.processor_id = None
        self.master = master

    def add(self, cmd, *args, **kw):
        """Put a command into queue for processing"""
        self.tasks.put((cmd, args, kw))

    def _schedule_processing(self):
        if self.processor_id is None:
            self.processor_id = self.master.after(
                self.delay, self.process_tasks
            )

    def process_tasks(self):
        try:
            while 1:
                data = self.tasks.get_nowait()
                cmd, args, kw = data
                cmd(*args, **kw)
        except queue.Empty:
            # print("No tasks pending.")
            pass
        self.processor_id = None
        self._schedule_processing()

    def start_processing(self):
        self._schedule_processing()


class LoaderTask(threading.Thread):
    """This represents a long running task"""

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app

    def run(self):
        """
        DO your thread safe coding here

        To update the UI,
        Send commands to the main app using self.app.task_cmd()
        """
        tasks = [
            ("Preparing images ...", 3),
            ("Creating custom theme ...", 2),
            ("Checking remote partner ...", 4),
            ("Finalizing ...", 2),
        ]
        for msg, seconds in tasks:
            print(msg)
            self.app.splash_update(msg)
            time.sleep(seconds)

        self.app.splash_finish()
