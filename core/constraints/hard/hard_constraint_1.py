from core.models import Schedule


def violates_hard_constraint_1(schedule: Schedule):
    """
    Hard Constraint 1: No two classes can take place in the same room at the same Timeslot.
    """
    unique_room_timeslot_pairs = []

    for c in schedule.classes:
        for unique_pair in unique_room_timeslot_pairs:
            if c.room.idx == unique_pair[0] and c.timeslot.idx == unique_pair[1]:
                return True

        unique_room_timeslot_pairs.append((c.room.idx, c.timeslot.idx))

    return False
