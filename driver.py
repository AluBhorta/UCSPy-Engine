import numpy as np

from data.data import COURSES, INSTRUCTORS, ROOMS, TIMESLOTS, NUM_OF_LECS_BEING_OFFERED
from data.generate_random_schedule import generate_random_schedule

from fitness.solution_encoding import encode, decode
from fitness.fitness import fitness, hard_penalty_multiplier, violates_a_hard_constraint
from fitness.constraints.hard_constraints import violates_hard_constraint_1, violates_hard_constraint_2, violates_hard_constraint_3, violates_hard_constraint_4
from fitness.constraints.soft_constraints import penalty_of_soft_constraint_1

from demo.numba_demo import numba_in_comparison

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
        ("\nCOURSES: %d (int course_id, str course_desc, int num_of_lectures, int[] preferred_rooms, int[] preferred_timeslots)\n" % len(COURSES)),
        COURSES
    )
    print(
        ("\nINSTRUCTORS: %d (int instuctor_id, str instuctor_desc, int[] qualified_courses, int[] available_timeslots, int[] preferred_rooms, int[] preferred_timeslots)\n" % len(INSTRUCTORS)),
        INSTRUCTORS
    )
    print("\nNUM_OF_LECS_BEING_OFFERED: \n", NUM_OF_LECS_BEING_OFFERED)


def check_fitness(iterations=100):
    '''check fitness for n iterations '''
    counter = 0

    for i in range(iterations):
        sch = generate_random_schedule()

        f = fitness(sch)
        if f > 0:
            print(f)
            counter += 1

    print("fitness(sch) > 0: %d times!" % counter)


def main():

    check_fitness(1024)
    # print_params()
    # print("\nNUM_OF_LECS_BEING_OFFERED: %d" % NUM_OF_LECS_BEING_OFFERED)


if __name__ == "__main__":
    main()
