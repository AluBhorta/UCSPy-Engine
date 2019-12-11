from fitness.constraints.hard_constraints import HARD_CONSTRAINTS
from fitness.constraints.soft_constraints import SOFT_CONSTRAINTS


def violates_a_hard_constraint(schedule) -> bool:
    for violates_hard_constraint in HARD_CONSTRAINTS:
        if violates_hard_constraint(schedule):
            return True

    return False


def hard_penalty_multiplier(schedule) -> int:
    if violates_a_hard_constraint(schedule):
        return 0
    else:
        return 1


def total_soft_penalty(schedule):
    total_penalty = 0

    for soft_penalty_i_of in SOFT_CONSTRAINTS:
        total_penalty += soft_penalty_i_of(schedule)

    return total_penalty


def fitness(schedule):
    hpm = hard_penalty_multiplier(schedule)
    tsp = total_soft_penalty(schedule)

    return hpm / (1 + tsp)
