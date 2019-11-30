"""
# Hard Constraints

if violatesHard:	return 0
else:				return 1 

## Constraints 

1. No two lectures can take place in the same room at the same Timeslot

2. No instructor can take more than one lecture at a given Timeslot

3. Instructors can only take certain courses they are qualified for
    - Lec[2] (course_id) should be in the list -> decode(Lec).instructor[1] (instructor.qualified_courses)

4. Instructors are only available at certain timeslots
    - Lec[1] (timeslot_id) should be in the list -> decode(Lec).instructor[2] (instructor.available_timeslots)


Schedule: (Room, Timeslot, Course, Instructor)[]

### How to add a hard constraint

- write a func that takes a Schedule as param
- perform desired violation check on Schedule
- if violates, return True else return False
- add your func to the list HARD_CONSTRAINTS at the end

"""
import numpy as np
from fitness.encode_decode import encode, decode


def violates_hc1(schedule):
    """
    Rule: No two lectures can take place in the same room at the same Timeslot
    """
    unique_room_slots = []

    for room_slot in schedule[:, 0:2]:
        for unique_room_slot in unique_room_slots:
            if np.array_equal(room_slot, unique_room_slot):
                return True

        unique_room_slots.append(room_slot)

    return False


def violates_hc2(schedule):
    """
    Rule: No instructor can take more than one lecture at a given Timeslot
    """
    unique_instr_slots = []

    for instr_slot in schedule[:, [1, 3]]:
        for unique_instr_slot in unique_instr_slots:
            if np.array_equal(instr_slot, unique_instr_slot):
                return True

        unique_instr_slots.append(instr_slot)

    return False


def violates_hc3(schedule):
    """
    Rule: Instructors can only take certain courses they are qualified for
    """
    for lec in schedule:
        course_id = lec[2]

        decoded_lec = decode(lec)
        qualified_courses = decoded_lec.instructor[1]

        if course_id not in qualified_courses:
            return True

    return False


def violates_hc4(schedule):
    pass


"""
Contains all the hard-constraint-funcs
"""
HARD_CONSTRAINTS = [violates_hc1, violates_hc2]
