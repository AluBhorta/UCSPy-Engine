
from core.models import Schedule, StateManager, Timeslot


def penalty_of_soft_constraint_6(schedule: Schedule, state: StateManager, unit_penalty=0.8, _inspect=False):
    """
    6. The Lab Section of a Course (if any) should be placed in adjacent Timeslots to the corresponding Theory Section.
    """

    def _get_classes_of_course(c_idx):
        return [c for c in schedule.classes
                if c.section.course.idx == c_idx]

    def _get_ajd_timeslot_idxs(t: Timeslot):
        out = []
        t1, t2 = t.idx-1, t.idx+1
        weekday = t.idx // state.num_of_daily_slots
        start_t_idx = weekday * state.num_of_daily_slots
        end_t_idx = ((weekday+1) * state.num_of_daily_slots) - 1
        if t1 >= start_t_idx:
            out.append(t1)
        if t2 <= end_t_idx:
            out.append(t2)
        return out

    violation_count = 0

    tl_pairs = state.tl_course_paris
    for pair in tl_pairs:
        theory_cls = _get_classes_of_course(pair[0])
        lab_cls = _get_classes_of_course(pair[1])
        for cls_pair in zip(theory_cls, lab_cls):
            theory_ts = cls_pair[0].timeslots
            lab_ts = cls_pair[1].timeslots
            theory_adj_ts_idxs = [_get_ajd_timeslot_idxs(t) for t in theory_ts]

            for _t in lab_ts:
                if _t not in theory_adj_ts_idxs:
                    violation_count += 1
                    if _inspect:
                        print(
                            f"Violation of SC6 ('The Lab Section of a Course (if any) should be placed in adjacent Timeslots to the corresponding Theory Section.') - of class: \n {cls_pair[1]}"
                        )
    return violation_count * unit_penalty
