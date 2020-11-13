import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as plticker
import bisect

from core.logging import UCSPLogger


def make_line_plot(log_file="data/logs/sample.log", ygap=1):
    """
    Plotter

    make plots to analyze performance of UCSP Solvers using saved log files auto generated from running Solver in `save_logs` mode.

    :param log_file: path to the log file.
    \n
    :param ygap: Amount of gap in the Y-axis ticks, as a mutiple of the average gap. A higher value gives less frequent ticks. (default: 5)

    N.B:

    - modifying the auto generated log files might not make Plotter work properly.
    \n
    """

    with open(log_file) as f:
        lines = f.read().split('\n')

        start = None
        for i in range(len(lines)):
            if lines[i].lower() == UCSPLogger.record_start_marker.lower():
                start = i+1
                break
        if not start:
            raise Exception('shit, no start marker found :/')

        end = None
        for i in range(len(lines)-1, 0, -1):
            if lines[i].lower() == UCSPLogger.record_end_marker.lower():
                end = i
                break
        if not end:
            raise Exception('shit, no end marker found :/')

        data = lines[start:end]
        plot_data = np.array([i.split('\t\t') for i in data])

        x, y = plot_data[:, 0], plot_data[:, 1]
        y = [float(i) for i in y]

        fig, ax = plt.subplots()
        ax.plot(x, y)

        ax.xaxis.set_major_locator(
            plticker.MultipleLocator(base=len(x)/10)
        )
        ybase = (min(y) + max(y)) / (len(y)) * ygap
        ax.yaxis.set_major_locator(
            plticker.MultipleLocator(base=ybase)
        )

        plt.title(f"Plotting from: {log_file}", fontsize=16)
        plt.xlabel("Generation", fontsize=15)
        plt.ylabel("Fitness", fontsize=15)
        plt.tick_params(labelsize=10)

        plt.grid()
        plt.show()
