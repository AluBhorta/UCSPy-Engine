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


def write_results_to_file(fname, results):
    f = open(fname, "w")
    for row in results[:, :2]:
        output = str(row[0]) + "," + str(row[1]) + "\n"
        f.write(output)
    f.close()


def do_bench(epochs, poplation_size):
    results = GA_for_UCSP(population_size=poplation_size, epochs=epochs)
    fname = "results/ga-results-e_%d-pop_%d.txt" % (epochs, poplation_size)

    write_results_to_file(fname, results)

    print("\nFinal Fitness %f" % fitness(results[-1, 2]))


def benching():
    # print_params()
    # epochs = 150
    # poplation_size = 1024

    # do_bench(epochs, poplation_size)
    # for i in range(3):
    #     do_bench(epochs, poplation_size)
    #     poplation_size = poplation_size * 2
        # epochs = epochs #* (i+1) * 2
    pass


def main():
    # print_params()
    epochs = 20
    poplation_size = 512

    results = GA_for_UCSP(population_size=poplation_size, epochs=epochs)
    # results = Memetic_for_UCSP(population_size=poplation_size, epochs=epochs)
    # results = PSO_for_UCSP(epochs=epochs, total_particles=poplation_size,)
    # results = Firefly_for_UCSP(population_size=poplation_size, epochs=epochs, )

    print("\nFinal Fitness %f" % fitness(results[-1, 2]))


if __name__ == "__main__":
    main()
