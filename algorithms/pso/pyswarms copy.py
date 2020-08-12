from copy import deepcopy
from numpy import array

from pyswarms.discrete.binary import BinaryPSO
from pyswarms.single.global_best import GlobalBestPSO

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
    # get_flat_sch = lambda: state.generate_schedule().flatten()
    # arr = array([get_flat_sch() for _ in range(10)])

    # # r = state.flat_fitness(arr[0])
    # r = state.flat_fitness_array(arr)
    # print(r)

    # exit(0)

    # TODO: implement new PSO from discrete base class or binaryPSO

    flat_sch = state.generate_schedule().flatten()

    dims = len(flat_sch)
    # print(flat_sch)

    len_sch = len(state.sections)

    f = state.flat_fitness(flat_sch)
    # print(f)

    limit_course = len(state.courses)
    limit_section = len(state.sections)
    limit_instructor = len(state.instructors)
    limit_room = len(state.rooms)
    limit_timeslot = len(state.timeslots)

    bound_low = array((0, 0, 0, 0, 0) * len_sch)
    bound_high = array((limit_course, limit_section,
                        limit_instructor, limit_room, limit_timeslot) * len_sch)
    bounds = (bound_low, bound_high)

    population_size = 10

    epochs = 100
    velocity_clamp = (0, 2)
    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9
               ,'k': population_size, 'p': 1
               }

    # sch = BinaryPSO(
    # sch = GlobalBestPSO(
    sch = IntegerPSO(
        n_particles=population_size,
        dimensions=dims,
        options=options,
        # bounds=bounds,
        # ftol=min_acceptable_fitness,
        # init_pos=flat_sch,

        # velocity_clamp=velocity_clamp
    ).optimize(state.flat_fitness_array, epochs)

    print(sch)
    exit(0)

    return sch
