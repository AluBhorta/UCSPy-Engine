# from core.models import Schedule


# def violates_hard_constraint_2(schedule: Schedule):
def violates_hard_constraint_2(schedule):
    """
    Hard Constraint 2: No instructor can take more than one lecture at a given Timeslot
    (I, T)
    """
    # (int instr_idx, int[] timeslot_idxs)[]
    unique_instr_timeslots = []

    for c in schedule.classes:
        for u_ITs in unique_instr_timeslots:
            if c.instructor.idx == u_ITs[0]:
                c_t_idxs = set(t.idx for t in c.timeslots)
                intersection = list(c_t_idxs.intersection(u_ITs[1]))
                if len(intersection) > 0:
                    return True

        unique_instr_timeslots.append(
            (c.instructor.idx, [t.idx for t in c.timeslots]))

    return False
