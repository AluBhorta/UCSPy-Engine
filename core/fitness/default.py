from core.models import Schedule, StateManager


def default_fitness(schedule: Schedule, state: StateManager, _inspect=False):
    def _hard_penalty_multiplier(schedule: Schedule, state: StateManager) -> int:
        def violates_a_hard_constraint(schedule: Schedule) -> bool:
            for hard_constraint in state.hard_constraints:
                if hard_constraint.violates(schedule):
                    return True
            return False

        if violates_a_hard_constraint(schedule):
            return 0
        else:
            return 1

    def _total_soft_penalty(schedule: Schedule, state: StateManager, _inspect=False):
        total_penalty = 0

        for soft_constraint in state.soft_constraints:
            total_penalty += soft_constraint.penalty_of(schedule, state, _inspect=_inspect)

        return total_penalty

    hpm = _hard_penalty_multiplier(schedule, state)
    tsp = _total_soft_penalty(schedule, state, _inspect)

    return hpm / (1 + tsp)
