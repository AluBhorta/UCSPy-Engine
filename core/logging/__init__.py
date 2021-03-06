
import sys
import datetime


class UCSPLogger(object):
    """  UCSPLogger

        used for logging to the console or to the log file and console.
    """
    record_start_marker = 'Generation\t\tFitness'
    record_end_marker = '->end<-'

    def __init__(self, save_logs=False):
        self.terminal = sys.stdout
        self.save_logs = save_logs

    def write(self, message):
        message = str(message) + "\n"
        self.terminal.write(message)

        if self.save_logs:
            if not hasattr(self, 'file'):
                self._create_file()

            self.file.write(message)

    def _create_file(self):
        t = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        fname = f"data/logs/{t}.log"
        self.file = open(fname, "w")
        print(f"Logging to file: {fname}")
