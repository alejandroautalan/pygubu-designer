import logging


class StatusBarHandler(logging.Handler):
    def __init__(self, app, level=logging.NOTSET):
        super().__init__(level)
        self.app = app
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s:%(message)s", datefmt="%H:%M:%S"
        )
        self.setFormatter(formatter)

    def emit(self, record):
        try:
            msg = self.format(record)
            self.app.log_message(msg, record.levelno)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException:
            self.handleError(record)
