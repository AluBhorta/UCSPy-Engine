
from core.models import Schedule, Timeslot, ScheduleParam


def penalty_of_soft_constraint_6(schedule: Schedule, schedule_param: ScheduleParam, unit_penalty, _inspect=False):
    """
    6. The Lab Section of a Course (if any) should be placed in a Timeslot that is before or after the corresponding Theory Section.
    """

    def _get_classes_of_course_idx(c_idx):
        return [c for c in schedule.classes
                if c.section.course.idx == c_idx]

    def _get_ajd_timeslot_idxs(t: Timeslot):
        # get valid days
        day_codes = ['ST', 'MW']
        if t.day_code == day_codes[0]:
            valid_days = ["S", "T"]
        elif t.day_code == day_codes[1]:
            valid_days = ["M", "W"]
        else:
            return []

        # get valid slots
        current_daily_slot_idx = None
        for i in range(len(schedule_param.daily_slots)):
            if t.daily_slot == schedule_param.daily_slots[i]:
                current_daily_slot_idx = i
                break
        if current_daily_slot_idx is not None:
            valid_slots = []
            if current_daily_slot_idx == 0:
                valid_slots.append(current_daily_slot_idx+1)
            elif current_daily_slot_idx == len(schedule_param.daily_slots)-1:
                valid_slots.append(current_daily_slot_idx-1)
            else:
                valid_slots.extend(
                    [current_daily_slot_idx-1, current_daily_slot_idx+1])
        else:
            raise Exception(
                f"ERROR! Invalid slot_idx of Timeslot {t} to have adjacent lab section.")

        # return valid timeslots
        valid_timeslot_idxs = []
        for timeslot in schedule_param.timeslots:
            if timeslot.day_code in valid_days and timeslot.daily_slot in valid_slots:
                valid_timeslot_idxs.append(timeslot.idx)

        return valid_timeslot_idxs

    def _get_theory_lab_course_idx_paris(courses):
        """ NOTE: for this to work, the Lab course should should be directly after its corresponding Theory course  in the `courses.csv` schedule_param
        TODO: replace the indexing strategy with a dedicated parameter in Course instance (e.g. C.lab_of_course_idx)
        """
        pairs = []
        for crs in courses:
            if crs.course_type.lower() == "lab":
                pairs.append((crs.idx-1, crs.idx))
        return pairs

    # start of penalty_of_soft_constraint_6
    violation_count = 0

    for pair in _get_theory_lab_course_idx_paris(schedule_param.courses):
        theory_cls = _get_classes_of_course_idx(pair[0])
        lab_cls = _get_classes_of_course_idx(pair[1])
        for theory_lab_pair in zip(theory_cls, lab_cls):
            theory_timeslot = theory_lab_pair[0].timeslot
            lab_timeslot = theory_lab_pair[1].timeslot

            theory_adj_ts_idxs = _get_ajd_timeslot_idxs(theory_timeslot)

            if len(theory_adj_ts_idxs) > 0 and lab_timeslot.idx not in theory_adj_ts_idxs:
                violation_count += 1
                if _inspect:
                    print(
                        f"Violation of SC6 ('The Lab Section of a Course (if any) should be placed in a Timeslot that is before or after the corresponding Theory Section.') - of class:\n\t{theory_lab_pair[1]}"
                    )
    return violation_count * unit_penalty
