import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as plticker
import bisect


def make_line_plot(log_file="data/logs/sample.log", ygap=5, start_line=4, end_line=-6):
    """
    Plotter

    make plots to analyze performance of UCSP Solvers using saved log files auto generated from running Solver in `save_logs` mode.

    :param log_file: path to the log file.
    \n
    :param ygap: Amount of gap in the Y-axis ticks, as a mutiple of the average gap. A higher value gives less frequent ticks. (default: 5)
    \n
    :param start_line: the line from which numeric Generation & Fitness log records start. Line numbers start from 1, not 0. (default: 4)
    \n
    :param end_line: the last line containing numeric Generation & Fitness log records. A negative number represents order in reverse direction. Line numbers start from 1, not 0. (default: -6)

    N.B:

    - modifying the auto generated log files might not make Plotter work properly.
    \n
    """
    with open(log_file) as f:
        start_line = start_line-1
        end_line = end_line-1

        data = f.read().split('\n')[start_line:end_line]
        plot_data = np.array([i.split('\t\t') for i in data])

        x, y = plot_data[:, 0], plot_data[:, 1]
        y = [float(i) for i in y]

        fig, ax = plt.subplots()
        ax.plot(x, y)

        ax.xaxis.set_major_locator(
            plticker.MultipleLocator(base=len(x)/10)
        )
        ybase = (min(y) + max(y)) / (len(y)) * ygap
        # print(ybase)
        ax.yaxis.set_major_locator(
            plticker.MultipleLocator(base=ybase)
        )

        plt.title(f"Plotting from: {log_file}")
        plt.xlabel("Generation")
        plt.ylabel("Fitness")

        plt.grid()
        plt.show()
