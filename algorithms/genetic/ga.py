import numpy as np
import random
from copy import deepcopy

from core.generators.generate_random_schedule import generate_random_schedule as grs
from core.models import StateManager, Schedule

def genetic_algorithm(
    state: StateManager,
    epochs=100,
    min_acceptable_fitness=1,
    population_size=100,
    elite_pct=10,
    mateable_pct=50,
    mutable_pct=5
):
    """ DEPRECATED: as it gives infeasible results. please refer to `algorithms/genetic/smart_mut_ga.py` for a workable verison of genetic_algorithm """
    
    population = [grs(state) for _ in range(population_size)]
    new_population = [None for _ in range(population_size)]

    total_classes = len(state.sections)

    print(f"Generation\t\tFitness")
    for epoch in range(epochs):
        """ Sort by its fitness in DESC order """
        population = sorted(
            population,
            key=lambda sch: state.fitness(sch),
            reverse=True)

        best_fitness = state.fitness(population[0])
        print(f"{epoch}\t\t{best_fitness}")

        if best_fitness >= min_acceptable_fitness:
            return population[0]

        """ Dominance by elites """
        elite_count = (elite_pct * population_size)//100
        for i in range(elite_count):
            new_population[i] = population[i]

        """ Crossover """
        mateable_count = (mateable_pct * population_size)//100
        siblig_index = 1 if (population_size - elite_count) % 2 == 0 else -1
        for i in range(elite_count, population_size, 2):
            parent1_idx = np.random.randint(mateable_count)
            parent2_idx = np.random.randint(mateable_count)

            # single point crossover
            crossover_point = np.random.randint(total_classes)

            # 2 children produced
            new_population[i + siblig_index] = Schedule(
                (population[parent1_idx].classes[:crossover_point] +
                 population[parent2_idx].classes[crossover_point:])
            )
            new_population[i] = Schedule(
                (population[parent2_idx].classes[:crossover_point] +
                 population[parent1_idx].classes[crossover_point:])
            )

        """ Mutation """
        mutable_count = (mutable_pct * population_size)//100
        for i in range(mutable_count):
            schedule_idx = np.random.randint(elite_count, population_size)
            class_idx = np.random.randint(total_classes)

            param_idx = np.random.randint(3)

            if param_idx == 0:
                """ mutate room """
                new_population[schedule_idx].classes[class_idx].room = random.choice(state.rooms)
            elif param_idx == 1:
                """ mutate instructor """
                new_population[schedule_idx].classes[class_idx].instructor = \
                    random.choice(state.instructors)
            else: # param_idx == 2
                """ mutate timeslots """
                l = len(new_population[schedule_idx].classes[class_idx].timeslots)
                new_population[schedule_idx].classes[class_idx].timeslots = \
                    random.choices(state.timeslots, k=l)

        population = new_population

    best_fitness = state.fitness(population[0])
    best_fit_idx = 0
    for i in range(1, len(population)):
        f = state.fitness(population[i])
        if f > best_fitness:
            best_fitness = f
            best_fit_idx = i

    return population[best_fit_idx]
