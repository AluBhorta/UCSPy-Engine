import numpy as np

from data.data import NUM_OF_ROOMS as R, NUM_OF_TIMELSOTS as T, NUM_OF_COURSES as C, NUM_OF_INSTRUCTORS as I, NUM_OF_LECS_BEING_OFFERED as L
from fitness.fitness import fitness
from data.rand_schedule_generators.grs_v1 import generate_random_schedule as grs


def GA_for_UCSP(epochs=50, min_acceptable_fitness=0.9, population_size=256, elite_pct=10, mateable_pct=50, mutable_pct=10, total_lectures=L):
    population = [None for _ in range(population_size)]

    for i in range(population_size):
        population[i] = grs()

    epoch = 0

    new_population = [None for _ in range(population_size)]
    
    # 0: Generation, 1: Fitness, 2: Schedule
    # results = np.array([[None, None, None] for i in range(epochs)])
    while epoch < epochs:

        population = sorted(
            population, key=lambda sch: fitness(sch), reverse=True)

        best_fitness = fitness(population[0])
        print("Generation: %d \t Fitness: %f " %
              (epoch, best_fitness))
        # results[epoch][0] = epoch
        # results[epoch][1] = best_fitness
        # results[epoch][2] = population[0]

        if best_fitness >= min_acceptable_fitness:
            return population[0]

        # Selection (of elites)
        elite_count = (elite_pct * population_size)//100
        for i in range(elite_count):
            new_population[i] = population[i]

        # Crossover
        mateable_count = (mateable_pct * population_size)//100
        siblig_index = 1 if (population_size - elite_count) % 2 == 0 else -1
        for i in range(elite_count, population_size, 2):
            parent1_idx = np.random.randint(mateable_count)
            parent2_idx = np.random.randint(mateable_count)

            # single point crossover
            crossover_point = np.random.randint(total_lectures)

            # 2 children produced
            new_population[i + siblig_index] = np.concatenate(
                (population[parent1_idx][:crossover_point], population[parent2_idx][crossover_point:]))
            new_population[i] = np.concatenate(
                (population[parent2_idx][:crossover_point], population[parent1_idx][crossover_point:]))

        # Mutation
        mutable_count = (mutable_pct * population_size)//100
        for i in range(mutable_count):
            schedule_idx = np.random.randint(elite_count, population_size)
            lec_idx = np.random.randint(total_lectures)
            param_idx = np.random.randint(4)

            if param_idx == 0:
                limit = R
            elif param_idx == 1:
                limit = T
            elif param_idx == 2:
                limit = C
            elif param_idx == 3:
                limit = I
            else:
                raise Exception("Error! Invalid param index!")

            new_population[schedule_idx][lec_idx][param_idx] = np.random.randint(
                limit)

        population = new_population

        epoch += 1

    best_fitness = fitness(population[0])
    best_fit_idx = 0
    for i in range(1, len(population)):
        f = fitness(population[i])
        # print("i: %d \tf: %f"%(i, f))
        if f > best_fitness:
            best_fitness = f
            best_fit_idx = i

    return population[best_fit_idx]
    # return results
