
from core.models import Schedule, ScheduleParam


def penalty_of_soft_constraint_7(schedule: Schedule, schedule_param: ScheduleParam, unit_penalty, _inspect=False):
    """
    7. Instructors have minimum credit load requirements.
    """
    violation_count = 0
    loads = dict()

    for c in schedule.classes:
        if not loads.get(c.instructor.idx):
            loads[c.instructor.idx] = c.section.course.credits
        else:
            loads[c.instructor.idx] += c.section.course.credits

    for idx in loads.keys():
        I = schedule_param.get_instructor(idx)
        if loads[idx] < I.min_credit_req:
            violation_count += 1
            if _inspect:
                print(
                    f"Violation of SC7 ('Instructors have minimum credit load requirements.') - Required: {I.min_credit_req}, Assigned: {loads[idx]} - of instructor:\n\t{I}.\n"
                )

    return violation_count * unit_penalty
