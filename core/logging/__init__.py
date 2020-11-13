
import sys
import datetime


class UCSPLogger(object):
    """  UCSPLogger

        used for logging to the console or to the log file and console.
    """

    def __init__(self, save_logs=False):
        self.terminal = sys.stdout
        self.save_logs = save_logs

    def write(self, message):
        message = str(message) + "\n"
        self.terminal.write(message)

        if self.save_logs:
            if not hasattr(self, 'file'):
                t = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
                fname = f"data/logs/{t}.log"
                self.file = open(fname, "w")
                print(f"Logging to file: {fname}")

            self.file.write(message)
