import numpy as np
from models.models import Lecture, Course, Instructor, Room, Timeslot
from data.data import COURSES, INSTRUCTORS, ROOMS, TIMESLOTS
from data.generate_random_schedule import generate_random_schedule
from fitness.encode_decode import encode, decode
from fitness.fitness import fitness, hard_penalty_multiplier, violates_a_hard_constraint
from fitness.constraints.hard_constraints import violates_hard_constraint_1, violates_hard_constraint_2, violates_hard_constraint_3, violates_hard_constraint_4


def print_inputs():
    print("\nROOMS: (str room_id) \n", ROOMS)
    print("\nTIMESLOTS: (str timeslot_id) \n", TIMESLOTS)
    print("\nCOURSES: (str course_id, int num_of_lectures, int[] preferred_rooms)\n", COURSES)
    print("\nINSTRUCTORS: (str instuctor_id, int[] qualified_courses, int[] available_timeslots)\n", INSTRUCTORS)


def check_constraints(sch):
    hc1 = violates_hard_constraint_1(sch)
    hc2 = violates_hard_constraint_2(sch)
    hc3 = violates_hard_constraint_3(sch)
    hc4 = violates_hard_constraint_4(sch)

    out = ""
    if not hc1:
        out += "yay, no VHC1!"
    if not hc2:
        out += "\tyay, no VHC2!"
    if not hc3:
        out += "\tyay, no VHC3!"
    if not hc4:
        out += "\tyay, no VHC4!"

    print(out)


def main():
    hc1_counter = 0
    hc2_counter = 0
    hc3_counter = 0
    hc4_counter = 0
    for i in range(1000):
        sch = generate_random_schedule()
        
        if not violates_hard_constraint_1(sch):
            hc1_counter += 1
        if not violates_hard_constraint_2(sch):
            hc2_counter += 1
        if not violates_hard_constraint_3(sch):
            hc3_counter += 1
        if not violates_hard_constraint_4(sch):
            hc4_counter += 1
    
    print(hc1_counter)
    print(hc2_counter)
    print(hc3_counter)
    print(hc4_counter)


if __name__ == "__main__":
    main()
