import numpy as np

from data.data import NUM_OF_ROOMS as R, NUM_OF_TIMELSOTS as T, NUM_OF_COURSES as C, NUM_OF_INSTRUCTORS as I, NUM_OF_LECS_BEING_OFFERED as L
from fitness.fitness import fitness
from data.generate_random_schedule import generate_random_schedule


def individual_local_search(sch, max_iter=50, total_lectures=L):
    count = 0
    past_fitness = fitness(sch)
    while count < max_iter:
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

        sch[lec_idx][param_idx] = np.random.randint(limit)
        if fitness(sch) > past_fitness:
            return sch
        count += 1
    return sch


def Memetic_for_UCSP(epochs=20, min_acceptable_fitness=0.5, population_size=256, elite_pct=10, mateable_pct=50, mutable_pct=10, local_search_pct=20, max_local_search_iter=50, total_lectures=L):
    population = [None for _ in range(population_size)]

    for i in range(population_size):
        population[i] = generate_random_schedule()

    generation_number = 0

    while generation_number < epochs:
        population = sorted(population, key=lambda s: fitness(s), reverse=True)

        best_fitness = fitness(population[0])
        print("Generation: %d \t Fitness: %f " %
              (generation_number, best_fitness))

        if best_fitness >= min_acceptable_fitness:
            return population[0]

        new_population = [None for _ in range(population_size)]

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

        # Local Search
        local_search_count = (local_search_pct * population_size)//100
        for i in range(local_search_count):
            schedule_idx = np.random.randint(population_size)
            new_population[schedule_idx] = individual_local_search(
                population[schedule_idx], max_local_search_iter)

        population = new_population

        generation_number += 1

    best_fitness = fitness(population[0])
    best_fit_idx = 0
    for i in range(1, len(population)):
        f = fitness(population[i])
        # print("i: %d \tf: %f"%(i, f))
        if f > best_fitness:
            best_fitness = f
            best_fit_idx = i

    return population[best_fit_idx]
