# from core.models import Schedule


# def violates_hard_constraint_1(schedule: Schedule):
def violates_hard_constraint_1(schedule):
    """
    Hard Constraint 1: No two lectures can take place in the same room at the same Timeslot
    (R, T)
    """
    # (int room_idx, int[] timeslot_idxs)[]
    unique_room_timeslots = []

    for c in schedule.classes:
        for u_RTs in unique_room_timeslots:
            if c.room.idx == u_RTs[0]:
                c_t_idxs = set(t.idx for t in c.timeslots)
                intersection = list(c_t_idxs.intersection(u_RTs[1]))
                if len(intersection) > 0:
                    return True

        unique_room_timeslots.append(
            (c.room.idx, [t.idx for t in c.timeslots]))

    return False
