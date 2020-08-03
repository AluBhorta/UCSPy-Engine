
# from core.models import Schedule


# def penalty_of_soft_constraint_3(schedule: Schedule, unit_penalty=0.6, _inspect=False):
def penalty_of_soft_constraint_3(schedule, state, unit_penalty=0.6, _inspect=False):
    """
    3. CourseGroups have Timeslot preferences. 
    (CG.preferred_timeslot_idxs)
    """
    violation_count = 0
    for c in schedule.classes:
        cg_idx = None
        for cg in state.course_groups:
            if c.section.course.idx in cg.course_idxs:
                cg_idx = cg.idx
                break
        if cg_idx:
            c_t_idxs = [t.idx for t in c.timeslots]
            for ct in c_t_idxs:
                if ct not in state.course_groups[cg_idx].preferred_timeslot_idxs:
                    violation_count += 1
                    if _inspect:
                        print(
                            f"Violation of SC3 ('CourseGroups have Timeslot preferences') - of class: \n {c}"
                        )
                    break

    return violation_count * unit_penalty
