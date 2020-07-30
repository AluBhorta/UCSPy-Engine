
# from core.models import Schedule


# def penalty_of_soft_constraint_4(schedule: Schedule, unit_penalty=0.5, _inspect=False):
def penalty_of_soft_constraint_4(schedule, unit_penalty=0.5, _inspect=False):
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
                if _inspect:
                    print(
                        f"Violation of SC4 ('Instructors have Timeslot preferences') - of class: \n {c}"
                    )
                break

    return violation_count * unit_penalty
