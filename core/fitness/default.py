from core.models import Schedule, StateManager


def _hard_penalty_multiplier(schedule: Schedule, state: StateManager, _inspect=False) -> int:
    def violates_a_hard_constraint(schedule: Schedule) -> bool:
        for hard_constraint in state.hard_constraints:
            if hard_constraint.violates(schedule):
                if _inspect:
                    print(
                        f"# Hard Constraint {hard_constraint._id} Violation ('{hard_constraint.desc}' !")
                return True
        return False

    if violates_a_hard_constraint(schedule):
        return 0
    else:
        return 1


def _total_soft_penalty(schedule: Schedule, state: StateManager, _inspect=False):
    total_penalty = 0

    for soft_constraint in state.soft_constraints:
        total_penalty += soft_constraint.penalty_of(
            schedule, state, _inspect=_inspect)

    return total_penalty


def default_fitness(schedule: Schedule, state: StateManager, _inspect=False):
    hpm = _hard_penalty_multiplier(schedule, state, _inspect)
    tsp = _total_soft_penalty(schedule, state, _inspect)

    return hpm / (1 + tsp)
