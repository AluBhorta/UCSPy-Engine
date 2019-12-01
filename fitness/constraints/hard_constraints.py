"""
# Hard Constraints

if violatesHard:	return 0
else:				return 1 

## Constraints 

1. No two lectures can take place in the same room at the same Timeslot

2. No instructor can take more than one lecture at a given Timeslot

3. Instructors can only take certain courses they are qualified for
    - Lec[2] (course_id) should be in the list -> decode(Lec)[3][1] (instructor.qualified_courses)

4. Instructors are only available at certain timeslots
    - Lec[1] (timeslot_id) should be in the list -> decode(Lec)[3][2] (instructor.available_timeslots)



Schedule: (Room, Timeslot, Course, Instructor)[]

### How to add a hard constraint

- write a func that takes a Schedule as param
- perform desired violation check on Schedule
- if violates, return True else return False
- add your func to the list HARD_CONSTRAINTS at the end

"""
import numpy as np
from fitness.encode_decode import decode


def violates_hard_constraint_1(schedule):
    """
    Hard Constraint 1: No two lectures can take place in the same room at the same Timeslot
    """
    unique_room_timeslots = []

    for room_slot in schedule[:, 0:2]:
        for unique_room_slot in unique_room_timeslots:
            if np.array_equal(room_slot, unique_room_slot):
                return True

        unique_room_timeslots.append(room_slot)

    return False


def violates_hard_constraint_2(schedule):
    """
    Hard Constraint 2: No instructor can take more than one lecture at a given Timeslot
    """
    unique_instr_timeslots = []

    for instr_slot in schedule[:, [1, 3]]:
        for unique_instr_slot in unique_instr_timeslots:
            if np.array_equal(instr_slot, unique_instr_slot):
                return True

        unique_instr_timeslots.append(instr_slot)

    return False


def violates_hard_constraint_3(schedule):
    """
    Hard Constraint 3: Instructors can only take certain courses they are qualified for
    """
    for lec in schedule:
        course_id = lec[2]

        decoded_lec = decode(lec)
        qualified_courses = decoded_lec[3][2]

        if course_id not in qualified_courses:
            return True

    return False


def violates_hard_constraint_4(schedule):
    """
    Hard Constraint 4: Instructors are only available at certain timeslots
    """
    for lec in schedule:
        timeslot_id = lec[1]

        decoded_lec = decode(lec)
        available_timeslots = decoded_lec[3][3]

        if timeslot_id not in available_timeslots:
            return True

    return False


"""
Contains all the hard-constraint-funcs
"""
HARD_CONSTRAINTS = [violates_hard_constraint_1, violates_hard_constraint_2, violates_hard_constraint_3, violates_hard_constraint_4]
