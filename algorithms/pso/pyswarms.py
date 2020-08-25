from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt
import pyswarms.utils.functions.single_obj as fx
from pyswarms.utils.plotters.plotters import plot_contour, plot_surface, plot_cost_history
from pyswarms.utils.plotters.formatters import Mesher, Designer
from pyswarms.utils.decorators import cost

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

    @cost
    def default_cost_func(x, **kwargs):
        return state.flat_fitness(x)

    # def default_cost_func(x, **kwargs):
    #     return np.array(
    #         [state.flat_fitness(i) for i in x]
    #     )

    len_course = len(state.courses)
    len_section = len(state.sections)
    len_instructor = len(state.instructors)
    len_room = len(state.rooms)
    len_timeslot = len(state.timeslots)

    bound_low = np.array((0, 0, 0, 0, 0) * len_section)
    bound_high = np.array((len_course, len_section,
                           len_instructor, len_room, len_timeslot) * len_section)
    bounds = (bound_low, bound_high)

    dims = len_section * 5
    population_size = 10
    epochs = 1000
    velocity_clamp = (-2, 10)
    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9, 'k': population_size, 'p': 1}

    init_pos = np.array([state.generate_schedule().flatten()
                         for _ in range(population_size)])

    # print(np.min(init_pos), np.max(init_pos))
    # exit()

    optimizer = IntegerPSO(
        n_particles=population_size,
        dimensions=dims,
        options=options,
        bounds=bounds,
        bh_strategy="nearest",
        init_pos=init_pos,
        velocity_clamp=velocity_clamp,
        # vh_strategy="unmodified",
        # ftol=-np.inf,
    )
    output = optimizer.optimize(default_cost_func, epochs, n_processes=None)
    # output = optimizer.optimize(fx.sphere, epochs, n_processes=None)

    # plot_cost_history(optimizer.cost_history)
    # _plot_performance(optimizer.pos_history)
    # plt.show()

    # print(output)
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
    animation3d = plot_surface(
        pos_history=pos_history_3d,
        mesher=m,
        designer=d,
        mark=(0, 0, 0)
    )
