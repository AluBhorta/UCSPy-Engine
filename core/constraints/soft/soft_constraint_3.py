
from core.models import Schedule, ScheduleParam


def penalty_of_soft_constraint_3(schedule: Schedule, schedule_param: ScheduleParam, unit_penalty, _inspect=False):
    """
    3. CourseGroups have Timeslot preferences.
    """
    violation_count = 0
    for c in schedule.classes:
        cg_idx = None
        for cg in schedule_param.course_groups:
            if c.section.course.idx in cg.course_idxs:
                cg_idx = cg.idx
                break
        if cg_idx is not None:
            if not c.timeslot.idx in schedule_param.course_groups[cg_idx].preferred_timeslot_idxs:
                violation_count += 1
                if _inspect:
                    print(
                        f"Violation of SC3 ('CourseGroups have Timeslot preferences') - of class:\n\t{c}"
                    )
        else:
            raise Exception(f"ERROR! No CourseGroup found for Class {c}!")

    return violation_count * unit_penalty
