from core.models import Schedule, StateManager

def penalty_of_soft_constraint_5(schedule: Schedule, state: StateManager, unit_penalty=0.8, _inspect=False):
    """
    5. Lectures of the same Class (of a Course) should be taken at one day intervals, if the Course has 2 lectures_per_week and 1 timeslots_per_lecture.
    """

    def _get_1d_ajd_timeslot_idxs(t_idx, number_of_daily_slots, total_ts):
        adj = number_of_daily_slots * 2
        out = []
        _t = t_idx - adj
        if _t >= 0:
            out.append(_t)
        _t = t_idx + adj
        if _t < total_ts:
            out.append(_t)
        return out

    violation_count = 0

    for c in schedule.classes:
        if c.section.course.lectures_per_week == 2 and c.section.course.timeslots_per_lecture == 1:
            adj_ts_idxs = _get_1d_ajd_timeslot_idxs(
                c.timeslots[0].idx,
                state.num_of_daily_slots,
                len(state.timeslots)
            )
            if c.timeslots[1].idx not in adj_ts_idxs:
                violation_count += 1
                if _inspect:
                    print(
                        f"Violation of SC5 ('Lectures of the same Class (of a Course) should be taken at one day intervals, if the Course has 2 lectures_per_week and 1 timeslots_per_lecture.') - of class:\n\t{c}"
                    )

    return violation_count * unit_penalty
