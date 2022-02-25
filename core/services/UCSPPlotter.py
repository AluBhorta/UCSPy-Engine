import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as plticker

from core.logging import UCSPLogger


class UCSPPlotter:
    """
    UCSPPlotter

    make plots to analyze performance of UCSP Solvers using saved log files auto generated from running Solver in `save_logs` mode.

    :param log_file: path to the log file.

    N.B:

    - modifying the auto generated log files might not make Plotter work properly.
    \n
    """

    def __init__(self, log_file="data/logs/sample.log"):
        self.log_file = log_file

    def plot(self, should_wait=True, *args, **kwargs):
        with open(self.log_file, 'r') as f:
            lines = f.read().split('\n')
            x, y = self._get_processed_axes(lines)

            _, ax = plt.subplots()
            ax.plot(x, y)

            ax.xaxis.set_major_locator(
                plticker.MultipleLocator(base=len(x)/10)
            )

            plt.title(f"Plotting from: {self.log_file}", fontsize=16)
            plt.xlabel("Generation", fontsize=15)
            plt.ylabel("Fitness", fontsize=15)
            plt.tick_params(labelsize=10)

            plt.grid()
            plt.show(block=should_wait)

    def _get_processed_axes(self, lines):
        start, end = self._get_start_and_end(lines)

        data = lines[start:end]
        plot_data = np.array([i.split('\t\t') for i in data])
        x, y = plot_data[:, 0], plot_data[:, 1]
        y = [float(i) for i in y]

        return x, y

    def _get_start_and_end(self, lines):
        start = None
        for i in range(len(lines)):
            if lines[i].lower() == UCSPLogger.record_start_marker.lower():
                start = i+1
                break
        if not start:
            raise Exception('ERROR! No start marker found :/')

        end = None
        for i in range(len(lines)-1, 0, -1):
            if lines[i].lower() == UCSPLogger.record_end_marker.lower():
                end = i
                break
        if not end:
            raise Exception('ERROR! No end marker found :/')

        return start, end
