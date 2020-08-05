
# from core.models import Schedule


# def penalty_of_soft_constraint_1(schedule: Schedule, unit_penalty=0.9, _inspect=False):
def penalty_of_soft_constraint_1(schedule, state, unit_penalty=0.9, _inspect=False):
    """
    1. Instructors should only take certain courses they are are assigned to
    (I.assigned_course_idxs)
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
