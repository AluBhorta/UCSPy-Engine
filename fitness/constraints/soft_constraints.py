
from data.models import Schedule


def penalty_of_soft_constraint_1(schedule: Schedule, unit_penalty=0.9):
    """
    1. Instructors should only take certain courses they are are assigned to
    (I.assigned_course_idxs)
    """
    violation_count = 0
    for c in schedule.classes:
        if c.section.course.idx not in c.instructor.assigned_course_idxs:
            violation_count += 1

    return violation_count * unit_penalty


def penalty_of_soft_constraint_2(schedule: Schedule, unit_penalty=0.85):
    """
    2. A particular Room should only allow Classes of certain Courses		
    (R.allowed_course_idxs)
    """
    violation_count = 0
    for c in schedule.classes:
        if c.section.course.idx not in c.room.allowed_course_idxs:
            violation_count += 1

    return violation_count * unit_penalty


def penalty_of_soft_constraint_3(schedule: Schedule, unit_penalty=0.6):
    """
    3. CourseGroups have Timeslot preferences. 
    (CG.preferred_timeslot_idxs)
    """
    violation_count = 0
    for c in schedule.classes:
        cg_idx = None
        for cg in schedule.course_groups:
            if c.section.course.idx in cg.course_idxs:
                cg_idx = cg.idx
                break
        if cg_idx:
            c_t_idxs = [t.idx for t in c.timeslots]
            for ct in c_t_idxs:
                if ct not in schedule.course_groups[cg_idx].preferred_timeslot_idxs:
                    violation_count += 1
                    break

    return violation_count * unit_penalty


def penalty_of_soft_constraint_4(schedule: Schedule, unit_penalty=0.5):
    """
    4. Instructors have Timeslot preferences.
    (I.preferred_timeslot_idxs)

    """
    violation_count = 0
    for c in schedule.classes:
        c_t_idxs = [t.idx for t in c.timeslots]
        for ct in c_t_idxs:
            if ct not in c.instructor.preferred_timeslot_idxs:
                violation_count += 1
                break

    return violation_count * unit_penalty


"""
Contains all the soft-constraint-funcs
"""
SOFT_CONSTRAINTS = [
    penalty_of_soft_constraint_1,
    penalty_of_soft_constraint_2,
    penalty_of_soft_constraint_3,
    penalty_of_soft_constraint_4,
]
