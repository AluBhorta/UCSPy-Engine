"""
unit_penalty: the penalty for violating a particular soft_constraint once. Also 
1 <= unit_penalty <= 10

Encoded_Lecture: (Room, Timeslot, Course, Instructor)
    (int room_idx, int timeslot_idx, int course_idx, int instructor_id)

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


def penalty_of_soft_constraint_1(schedule, unit_penalty=8):
    """
    [unit_penalty=7] Some Courses have Room preferences.
    """
    violation_count = 0
    for lec in schedule:
        room_idx = lec[0]
        preferred_rooms = decode(lec)[2][3]

        if room_idx not in preferred_rooms:
            violation_count += 1

    return violation_count * unit_penalty


def penalty_of_soft_constraint_2(schedule, unit_penalty=4):
    """
    [unit_penalty=7] Some Instructors have Room preferences.
    """
    violation_count = 0
    for lec in schedule:
        room_idx = lec[0]
        preferred_rooms = decode(lec)[3][4]

        if room_idx not in preferred_rooms:
            violation_count += 1

    return violation_count * unit_penalty


def penalty_of_soft_constraint_3(schedule, unit_penalty=9):
    """
    [unit_penalty=9] Some Courses have Timeslot preferences.
    """
    violation_count = 0
    for lec in schedule:
        timeslot_idx = lec[1]
        preferred_timeslots = decode(lec)[2][4]

        if timeslot_idx not in preferred_timeslots:
            violation_count += 1

    return violation_count * unit_penalty



def penalty_of_soft_constraint_4(schedule, unit_penalty=6):
    """
    [unit_penalty=6] Instructors have Timeslot preferences. 
    """
    violation_count = 0
    for lec in schedule:
        timeslot_idx = lec[1]
        preferred_timeslots = decode(lec)[3][5]

        if timeslot_idx not in preferred_timeslots:
            violation_count += 1

    return violation_count * unit_penalty


"""
Contains all the soft-constraint-funcs
"""
SOFT_CONSTRAINTS = [
    penalty_of_soft_constraint_1,
    penalty_of_soft_constraint_2,
    penalty_of_soft_constraint_3,
    penalty_of_soft_constraint_4,
]
