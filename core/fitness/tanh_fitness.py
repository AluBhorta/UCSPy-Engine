import numpy as np

from core.models import Schedule, StateManager


def _violates_a_hard_constraint(schedule: Schedule, state: StateManager, _inspect=False) -> bool:
    for hard_constraint in state.hard_constraints:
        if hard_constraint.violates(schedule):
            if _inspect:
                print(
                    f"# Hard Constraint {hard_constraint._id} Violation ('{hard_constraint.desc}' !")
            return True
    return False


def _total_soft_penalty(schedule: Schedule, state: StateManager, _inspect=False):
    total_penalty = 0

    for soft_constraint in state.soft_constraints:
        total_penalty += soft_constraint.penalty_of(
            schedule, state, _inspect=_inspect)

    return total_penalty


def tanh_fitness(schedule: Schedule, state: StateManager, _inspect=False, relax_coeff=0.01):
    """
    Hyperbolic tangent fitness function.

    returns 1 if schedule infeasible, 0 if perfect. Otherwise results are in between 0 and 1 if the total soft penalty of the schedule > 0.

    `relax_coeff` determines how quickly tanh(x) will converge to 1 as x approaches infinity. The smaller the `relax_coeff`, the slower it'll converge.
    """
    violates_a_hc = _violates_a_hard_constraint(schedule, state, _inspect)
    if violates_a_hc:
        return 1

    tsp = _total_soft_penalty(schedule, state, _inspect)
    # print(tsp)
    if tsp < 0:
        raise Exception(f"Error! Total soft penalty cannot be negative!")
    return np.tanh(relax_coeff * tsp)
