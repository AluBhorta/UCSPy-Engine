"""
# Hard Constraints

if violatesHard:	return 0
else:				return 1 

## Constraints 

1. No two lectures can take place in the same room at the same Timeslot

2. No instructor can take more than one lecture at a given Timeslot

3. Instructors can only take certain courses they are qualified for


Schedule: (Room, Timeslot, Course, Instructor)[]
"""
import numpy as np


def violates_hc1(schedule):
    unique_room_slots = []

    for room_slot in schedule[:, 0:2]:
        for unique_room_slot in unique_room_slots:
            if np.array_equal(room_slot, unique_room_slot):
                return True

        unique_room_slots.append(room_slot)

    return False


def violates_hc2(schedule):
    unique_instr_slots = []

    for instr_slot in schedule[:, [1, 3]]:
        for unique_instr_slot in unique_instr_slots:
            if np.array_equal(instr_slot, unique_instr_slot):
                return True

        unique_instr_slots.append(instr_slot)

    return False


def violates_hc3(schedule):
    pass
