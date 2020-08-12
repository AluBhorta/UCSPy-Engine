from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt

from pyswarms.discrete.binary import BinaryPSO
from pyswarms.single.global_best import GlobalBestPSO
import pyswarms.utils.functions.single_obj as fx
from pyswarms.utils.plotters.plotters import plot_contour, plot_surface, plot_cost_history
# from pyswarms.utils.plotters.formatters import 
from pyswarms.utils.plotters.formatters import Mesher, Designer

from core.models import StateManager, Schedule
from core.logging import UCSPLogger
from .integer_pso import IntegerPSO


def pyswarms(
    logger: UCSPLogger,
    state: StateManager,
    epochs=100,
    population_size=100,
    min_acceptable_fitness=1,
    w0=0.8, wf=0.2, c1=1, c2=2, vmax_pct=5
):

    dims = 4
    population_size = 10
    epochs = 1000
    # velocity_clamp = (0, 2)
    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9, 'k': population_size, 'p': 1}

    optimizer = IntegerPSO(
    # optimizer = GlobalBestPSO(
        n_particles=population_size,
        dimensions=dims,
        options=options,
        # bounds=bounds,
        # ftol=min_acceptable_fitness,
        # init_pos=flat_sch,
        # velocity_clamp=velocity_clamp
    )
    output = optimizer.optimize(fx.ackley, epochs)

    # NOTE: IntegerPSO is not improving solution! :(

    # plot_cost_history(optimizer.cost_history)
    # _plot_performance(optimizer.pos_history)
    # plt.show()

    print(output)
    exit(0)

    return sch


def _plot_performance(pos_history):

    # Plot the sphere function's mesh for better plots
    m = Mesher(func=fx.sphere, limits=[(-1, 1), (-1, 1)])
    # Adjust figure limits
    d = Designer(limits=[(-1, 1), (-1, 1), (-0.1, 1)],
                 label=['x-axis', 'y-axis', 'z-axis'])

    # plot_contour(pos_history=optimizer.pos_history,mesher=m, designer=d, mark=(0, 0))

    pos_history_3d = m.compute_history_3d(pos_history)  # preprocessing
    animation3d = plot_surface(pos_history=pos_history_3d,
                               mesher=m, designer=d,
                            #    mark=(0, 0, 0)
                               )
