
# from core.models import Schedule


# def penalty_of_soft_constraint_2(schedule: Schedule, unit_penalty=0.85, _inspect=False):
def penalty_of_soft_constraint_2(schedule, state, unit_penalty=0.85, _inspect=False):
    """
    2. A particular Room should only allow Classes of certain Courses		
    (R.allowed_course_idxs)
    """
    violation_count = 0
    for c in schedule.classes:
        if c.section.course.idx not in c.room.allowed_course_idxs:
            violation_count += 1
            if _inspect:
                print(
                    f"Violation of SC2 ('A particular Room should only allow Classes of certain Courses') - of class: \n {c}"
                )

    return violation_count * unit_penalty
