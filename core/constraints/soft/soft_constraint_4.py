
from core.models import Schedule, StateManager


def penalty_of_soft_constraint_4(schedule: Schedule, state: StateManager, unit_penalty, _inspect=False):
    """
    4. Instructors have Timeslot preferences.
    """
    violation_count = 0
    for c in schedule.classes:
        if c.timeslot.idx not in c.instructor.preferred_timeslot_idxs:
            violation_count += 1
            if _inspect:
                print(
                    f"Violation of SC4 ('Instructors have Timeslot preferences') - of class:\n\t{c}"
                )

    return violation_count * unit_penalty
