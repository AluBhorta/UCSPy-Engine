
""" 

--save_sch=True
will save encoded final sch in 'data/sch' in a csv
which can then be used as the schedule by the org/uni

--save_logs
will record logs on screen
will auto 'save_sch' = True

--save_logs=True

transition results could be used for plotting and analysis using another cmd/flag?

"""

import sys
import datetime

class UCSPLogger(object):
    def __init__(self, save_logs=False):
        self.terminal = sys.stdout
        if save_logs:
            t = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
            fname = f"data/logs/{t}.log"
            self.file = open(fname, "w")
            print(f"Logging to file {fname}")
        else:
            self.file = False

    def write(self, message):
        message = str(message) + "\n"
        self.terminal.write(message)
        if self.file:
            self.file.write(message)

    def flush(self):
        pass
