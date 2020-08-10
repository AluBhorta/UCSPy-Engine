
from core.models import Schedule, StateManager


def penalty_of_soft_constraint_1(schedule: Schedule, state: StateManager, unit_penalty, _inspect=False):
    """
    1. Instructors should only take certain courses they are are assigned to.
    """
    violation_count = 0
    for c in schedule.classes:
        if c.section.course.idx not in c.instructor.assigned_course_idxs:
            violation_count += 1
            if _inspect:
                print(
                    f"Violation of SC1 ('Instructors should only take certain courses they are are assigned to') - of class:\n\t{c}"
                )

    return violation_count * unit_penalty
