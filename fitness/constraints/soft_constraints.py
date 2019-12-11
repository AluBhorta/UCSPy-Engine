"""
unit_penalty: the penalty for violating a particular soft_constraint once.

1. Some Courses have Room preferences. (i.e. Course.prefered_rooms)
- N.B: some courses might have 0 preffered_rooms, in that case, allow any room

2. Some Instructors have Room preferences.

3. Some Courses have Timeslot preferences.

4. Some Instructors have Timeslot preferences.

### How to add a soft constraint

- write a func that takes param: (Schedule S, int unit_penalty)
- perform desired violation check on Schedule
- count (e.g. n) the number of times S violates your constraint
- return (n * unit_penalty) from your func
- add your func to the list SOFT_CONSTRAINTS at the end

"""
from fitness.solution_encoding import decode


def penalty_of_soft_constraint_1(schedule, unit_penalty=7):
    """
    [unit_penalty=7] Some Courses have Room preferences.
    """
    violation_count = 0
    for lec in schedule:
        room_id = lec[0]
        preferred_rooms = decode(lec)[2][3]

        if room_id not in preferred_rooms:
            violation_count += 1

    return violation_count * unit_penalty


def penalty_of_soft_constraint_2(schedule):
    """
    [unit_penalty=_] Some Instructors have Room preferences.
    """
    pass


def penalty_of_soft_constraint_3(schedule):
    """
    [unit_penalty=_] Some Courses have Timeslot preferences.
    """
    pass


def penalty_of_soft_constraint_4(schedule):
    """
    [unit_penalty=_] Instructors have Timeslot preferences. 
    """
    pass


"""
Contains all the soft-constraint-funcs
"""
SOFT_CONSTRAINTS = [
    penalty_of_soft_constraint_1
]
