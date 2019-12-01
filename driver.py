import numpy as np
from models.models import Lecture, Course, Instructor, Room, Timeslot
from data.data import COURSES, INSTRUCTORS, ROOMS, TIMESLOTS, NUM_OF_LECS_BEING_OFFERED
from fitness.encode_decode import encode, decode
from fitness.fitness import fitness, hard_penalty_multiplier, violates_a_hard_constraint
from fitness.constraints.hard_constraints import violates_hard_constraint_1, violates_hard_constraint_2, violates_hard_constraint_3, violates_hard_constraint_4
from data.generate_random_schedule import naive_random_schedule, generate_random_schedule
from demo.numba_demo import numba_list_append


def print_params():
    print(
        ("\nROOMS: %d (int room_id, str room_desc) \n" % len(ROOMS)),
        ROOMS
    )
    print(
        ("\nTIMESLOTS: %d (int timeslot_id, str timeslot_desc) \n" % len(TIMESLOTS)),
        TIMESLOTS
    )
    print(
        ("\nCOURSES: %d (int course_id, str course_desc, int num_of_lectures, int[] preferred_rooms)\n" % len(COURSES)),
        COURSES
    )
    print(
        ("\nINSTRUCTORS: %d (int instuctor_id, str instuctor_desc, int[] qualified_courses, int[] available_timeslots)\n" % len(INSTRUCTORS)),
        INSTRUCTORS
    )
    print("\nNUM_OF_LECS_BEING_OFFERED: \n", NUM_OF_LECS_BEING_OFFERED)


def check_constraints(iterations=100):
    hc1_counter = 0
    hc2_counter = 0
    hc3_counter = 0
    hc4_counter = 0
    for i in range(iterations):
        sch = generate_random_schedule()

        if not violates_hard_constraint_1(sch):
            hc1_counter += 1
        if not violates_hard_constraint_2(sch):
            hc2_counter += 1
        if not violates_hard_constraint_3(sch):
            hc3_counter += 1
        if not violates_hard_constraint_4(sch):
            hc4_counter += 1

    print("hc1_counter: %d" % hc1_counter)
    print("hc2_counter: %d" % hc2_counter)
    print("hc3_counter: %d" % hc3_counter)
    print("hc4_counter: %d" % hc4_counter)


def main():
    print_params()

    # print("\nNUM_OF_LECS_BEING_OFFERED: %d" % NUM_OF_LECS_BEING_OFFERED)
    # check_constraints(3000)


if __name__ == "__main__":
    main()
