import numpy as np
# from matplotlib import pyplot as plt

from data.data import COURSES, INSTRUCTORS, ROOMS, TIMESLOTS, NUM_OF_LECS_BEING_OFFERED
from data.generate_random_schedule import generate_random_schedule
from fitness.fitness import fitness
from fitness.solution_encoding import encode, decode

from algorithms.GA.ga import GA_for_UCSP
from algorithms.Memetic.memetic import Memetic_for_UCSP
from algorithms.PSO.pso import PSO_for_UCSP
from algorithms.Firefly.firefly import Firefly_for_UCSP


def print_params():
    print(
        ("\nROOMS: %d (int room_idx, str room_desc) \n" % len(ROOMS)),
        ROOMS
    )
    print(
        ("\nTIMESLOTS: %d (int timeslot_idx, str timeslot_desc) \n" % len(TIMESLOTS)),
        TIMESLOTS
    )
    print(
        ("\nCOURSES: %d (int course_idx, str course_desc, int num_of_lectures, int[] preferred_rooms, int[] preferred_timeslots)\n" % len(COURSES)),
        COURSES
    )
    print(
        ("\nINSTRUCTORS: %d (int instuctor_idx, str instuctor_desc, int[] qualified_courses, int[] available_timeslots, int[] preferred_rooms, int[] preferred_timeslots)\n" % len(INSTRUCTORS)),
        INSTRUCTORS
    )
    print("\nNUM_OF_LECS_BEING_OFFERED: \n", NUM_OF_LECS_BEING_OFFERED)


def check_fitness(iterations=1000):
    '''check fitg_best_fitnessssions '''
    counter = 0

    for i in range(iterations):
        sch = generate_random_schedule()

        f = fitness(sch)
        fitnesses[i] = f
        if f > 0:
            # print(f)
            counter += 1

    print("fitness(sch) > 0: %d times!" % counter)


def pretty_print_schedule(sch):
    pass


def main():
    # sch = GA_for_UCSP(population_size=256, epochs=20, mutable_pct=30)
    # sch = Memetic_for_UCSP(population_size=256, epochs=20, mutable_pct=40)
    # sch = PSO_for_UCSP(epochs=20)
    sch = Firefly_for_UCSP(epochs=20)
    print("\nFinal Fitness %f" % fitness(sch))

    pass


if __name__ == "__main__":
    main()
