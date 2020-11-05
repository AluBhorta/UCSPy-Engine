
from core.models import Schedule, Timeslot, ScheduleParam
from core.util import _get_theory_lab_course_idx_paris, _get_classes_of_course_idx


def penalty_of_soft_constraint_7(schedule: Schedule, schedule_param: ScheduleParam, unit_penalty, _inspect=False):
    """
    7. The Lab Section of a Course (if any) should be placed in a Timeslot that is before or after the corresponding Theory Section.
    """

    violation_count = 0

    theory_lab_course_idx_paris = _get_theory_lab_course_idx_paris(
        schedule_param.courses
    )
    for pair in theory_lab_course_idx_paris:
        theory_cls = _get_classes_of_course_idx(pair[0], schedule)
        lab_cls = _get_classes_of_course_idx(pair[1], schedule)

        for theory_lab_pair in zip(theory_cls, lab_cls):
            theory_instr = theory_lab_pair[0].instructor
            lab_instr = theory_lab_pair[1].instructor

            if not theory_instr.idx == lab_instr.idx:
                violation_count += 1
                if _inspect:
                    print(
                        f"Violation of SC7 ('The Lab Section of a Course (if any) should be placed in a Timeslot that is before or after the corresponding Theory Section.') - of class:\n\t{theory_lab_pair[1]}"
                    )

    return violation_count * unit_penalty
