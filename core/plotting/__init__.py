from matplotlib import pyplot as plt
import numpy as np


def make_line_plot(file_path):
    """
    Plotter

    make plots from saved log files.
    """
    with open(file_path) as f:
        data = f.read().split('\n')[3:-3]
        plot_data = np.array([i.split('\t\t') for i in data])

        plt.plot(plot_data[:, 0], plot_data[:, 1])

        fn = file_path.split("/")[-1]
        plt.title(f"Plotting from {fn}")
        plt.xlabel("Generation")
        plt.ylabel("Fitness")

        plt.grid()

        plt.show()
