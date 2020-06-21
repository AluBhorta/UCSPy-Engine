from core.models import Schedule
from core.fitness.constraints.hard_constraints import HARD_CONSTRAINTS
from core.fitness.constraints.soft_constraints import SOFT_CONSTRAINTS


def hard_penalty_multiplier(schedule: Schedule) -> int:
    def violates_a_hard_constraint(schedule: Schedule) -> bool:
        for violates_hard_constraint in HARD_CONSTRAINTS:
            if violates_hard_constraint(schedule):
                return True
        return False

    if violates_a_hard_constraint(schedule):
        return 0
    else:
        return 1


def total_soft_penalty(schedule: Schedule):
    total_penalty = 0

    for soft_penalty_i_of in SOFT_CONSTRAINTS:
        total_penalty += soft_penalty_i_of(schedule)

    return total_penalty


def fitness(schedule: Schedule):
    hpm = hard_penalty_multiplier(schedule)
    tsp = total_soft_penalty(schedule)

    return hpm / (1 + tsp)
