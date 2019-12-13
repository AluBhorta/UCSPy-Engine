import numpy as np

from data.data import NUM_OF_ROOMS as R, NUM_OF_TIMELSOTS as T, NUM_OF_COURSES as C, NUM_OF_INSTRUCTORS as I, NUM_OF_LECS_BEING_OFFERED as L
from fitness.fitness import fitness
from data.generate_random_schedule import generate_random_schedule


def get_distance(sch1, sch2):
    pass


def Firefly_for_UCSP(epochs=100, min_acceptable_fitness=0.5, population_size=256, absorption_coeff=0.5):
    population = [None for _ in range(population_size)]

    for i in range(population_size):
        population[i] = generate_random_schedule()

    generation_number = 0
    while generation_number < epochs:

        # main cream

        generation_number += 1

    # return population[best_fit_idx]
