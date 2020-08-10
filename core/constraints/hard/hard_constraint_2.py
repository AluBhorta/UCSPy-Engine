from core.models import Schedule


def violates_hard_constraint_2(schedule: Schedule):
    """
    Hard Constraint 2: No Instructor can take more than one class at a given Timeslot.
    """
    unique_instr_timeslot_pairs = []

    for c in schedule.classes:
        for unique_pair in unique_instr_timeslot_pairs:
            if c.instructor.idx == unique_pair[0] and c.timeslot.idx == unique_pair[1]:
                return True

        unique_instr_timeslot_pairs.append((c.instructor.idx, c.timeslot.idx))

    return False
