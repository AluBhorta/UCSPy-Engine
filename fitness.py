
def violates_a_hard_constraint(lec) -> bool:
    # TODO
    pass


def hard_penalty_multiplier(lec) -> float:
    if violates_a_hard_constraint(lec):
        return 0
    else:
        return 1


def get_soft_constraint_count():
    # TODO
    pass


def violates_soft_constraint(constraint_index, lec):
    # TODO
    pass


def soft_penalty_value_of(constraint_index):
    # TODO
    pass


def get_soft_penalty_of(constraint_index, lec):
    if violates_soft_constraint(constraint_index, lec):
        return soft_penalty_value_of(constraint_index)
    else:
        return 0


def total_soft_penalty(lec):
    SC = get_soft_constraint_count()

    penalty = 0
    for constraint_index in range(SC):
        penalty += get_soft_penalty_of(constraint_index, lec)

    return penalty


def fitness(lec):
    hpm = hard_penalty_multiplier(lec)
    tsp = total_soft_penalty(lec)

    return hpm / (1 + tsp)
