from algorithms.GA.ga import GA_for_UCSP
from algorithms.Memetic.memetic import Memetic_for_UCSP
from algorithms.PSO.pso import PSO_for_UCSP
from algorithms.Firefly.firefly import Firefly_for_UCSP

from data.data import ROOMS as R, TIMESLOTS as T, COURSES as C, INSTRUCTORS as I, NUM_OF_LECS_BEING_OFFERED as L
from data.generate_random_schedule import generate_random_schedule, generate_random_schedule_v2 as grs2

from fitness.fitness import fitness


def get_algo(algo_name="ga"):
    if algo_name == "ga":
        return GA_for_UCSP
    elif algo_name == "meme":
        return Memetic_for_UCSP
    elif algo_name == "pso":
        return PSO_for_UCSP
    elif algo_name == "firefly":
        return Firefly_for_UCSP
    else:
        raise Exception("Error! algo_name not defined!")


""" v DEPRECATED v """


def print_params():
    print(
        ("\nROOMS: %d (int room_idx, str room_desc) \n" % len(R)), R)
    print(
        ("\nTIMESLOTS: %d (int timeslot_idx, str timeslot_desc) \n" % len(T)), T)
    print(
        ("\nCOURSES: %d (int course_idx, str course_desc, int num_of_lectures, int[] preferred_rooms, int[] preferred_timeslots)\n" % len(C)), C)
    print(
        ("\nINSTRUCTORS: %d (int instuctor_idx, str instuctor_desc, int[] qualified_courses, int[] available_timeslots, int[] preferred_rooms, int[] preferred_timeslots)\n" % len(I)), I)
    print("\nNUM_OF_LECS_BEING_OFFERED: \n", L)


def check_fitness(iterations=100):
    '''check fitness of randomly generated solutions of current UCSP instance'''
    counter = 0

    for i in range(iterations):
        sch = grs2()
        f = fitness(sch)
        print(f)

        if f > 0:
            counter += 1

    print("fitness(sch) > 0: %d times!" % counter)
