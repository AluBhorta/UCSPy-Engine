from fitness.constraints.hard_constraints import HARD_CONSTRAINTS


def violates_a_hard_constraint(schedule) -> bool:
    for violates_hard_constraint in HARD_CONSTRAINTS:
        if violates_hard_constraint(schedule):
            return True

    return False


def hard_penalty_multiplier(schedule) -> float:
    if violates_a_hard_constraint(schedule):
        return 0
    else:
        return 1


def get_soft_constraint_count():
    # TODO
    pass


def violates_soft_constraint(constraint_index, schedule):
    # TODO
    pass


def soft_penalty_value_of(constraint_index):
    # TODO
    pass


def get_soft_penalty_of(constraint_index, schedule):
    if violates_soft_constraint(constraint_index, schedule):
        return soft_penalty_value_of(constraint_index)
    else:
        return 0


def total_soft_penalty(schedule):
    """
    TODO: given a schedule, this func runs each soft-constraint-func in soft_constraints.py against the schedule, and returns a total-penalty-value >= 0
    each soft-constraint-func, taking the schedule, returns the penalty caused by violations of that particular soft constraint by the schedule. 
    each soft-constraint-func has a particular penalty value (0 <= val <= 9 || infinity?) to indicate the severity of violating that constraint (?once)
    the number of occurances of that violation in the schedule can cause the penalty to aggregate for that schedule.
    TODO(later) figure out a way to better mathematically weigh the penaltys of each occurance of a soft_constraint violation, so that they don't pile up too much unnecessarily. Consult a Faculty to figure out better math.
    """
    SC = get_soft_constraint_count()

    penalty = 0
    for constraint_index in range(SC):
        penalty += get_soft_penalty_of(constraint_index, schedule)

    return penalty


def fitness(schedule):
    hpm = hard_penalty_multiplier(schedule)
    tsp = total_soft_penalty(schedule)

    return hpm / (1 + tsp)
