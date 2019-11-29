
def violates_a_hard_constraint(schedule) -> bool:
    # TODO
    pass


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
    SC = get_soft_constraint_count()

    penalty = 0
    for constraint_index in range(SC):
        penalty += get_soft_penalty_of(constraint_index, schedule)

    return penalty


def fitness(schedule):
    hpm = hard_penalty_multiplier(schedule)
    tsp = total_soft_penalty(schedule)

    return hpm / (1 + tsp)
