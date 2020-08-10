
from core.models import Schedule, StateManager


def penalty_of_soft_constraint_5(schedule: Schedule, state: StateManager, unit_penalty, _inspect=False):
    """
    5. If a Course has 2 Lectures Per Week, it should take place in a composite Timeslot i.e. with Day code of 'ST' or 'MW'.
    """
    violation_count = 0

    for c in schedule.classes:
        if int(c.section.course.lectures_per_week) == 2:
            if c.timeslot.day_code not in ["ST", "MW"]:
                violation_count += 1
                if _inspect:
                    print(
                        f"Violation of SC5 ('If a Course has 2 Lectures Per Week, it should take place in a composite Timeslot i.e. with Day code of 'ST' or 'MW'.') - of class:\n\t{c}"
                    )

    return violation_count * unit_penalty
