import numpy as np
import random
from copy import deepcopy

from core.models import StateManager, Schedule
from core.logging import UCSPLogger
from core.models.Algorithm import Algorithm


class GeneticAlgorithm(Algorithm):
    def __init__(self, logger: UCSPLogger, state: StateManager):
        super(GeneticAlgorithm, self).__init__(
            logger,
            state,
            name="ga"
        )

    def run(self, *args, **kwargs):
        return _smart_mut_genetic_algorithm(
            self.logger,
            self.state,
            *args, **kwargs
        )


def _smart_mut_genetic_algorithm(
    logger: UCSPLogger,
    state: StateManager,
    epochs=100,
    population_size=100,
    min_acceptable_fitness=0,
    elite_pct=10,
    mateable_pct=50,
    mutable_pct=20
):
    # initial population
    population = [state.generate_schedule() for _ in range(population_size)]
    new_population = [None for _ in range(population_size)]

    total_classes = len(state.sections)
    logger.write(f"Generation\t\tFitness")

    for epoch in range(epochs):
        try:
            population = sorted(
                population,
                key=lambda sch: state.fitness(sch))

            best_fitness = state.fitness(population[0])
            logger.write(f"{epoch}\t\t{best_fitness}")

            if best_fitness <= min_acceptable_fitness:
                return population[0]

            """ Dominance by elites """
            elite_count = (elite_pct * population_size)//100
            for i in range(elite_count):
                new_population[i] = population[i]

            """ Crossover """
            mateable_count = (mateable_pct * population_size)//100
            siblig_index = 1 \
                if (population_size - elite_count) % 2 == 0 \
                else -1
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
                # NOTE: research on optimal choice of `schedule_idx` range
                schedule_idx = np.random.randint(population_size)
                # schedule_idx = np.random.randint(elite_count, population_size)

                class_idx = np.random.randint(total_classes)

                param_idx = np.random.randint(3)

                tmp_sch = deepcopy(new_population[schedule_idx])

                if param_idx == 0:
                    """ mutate room """
                    tmp_sch.classes[class_idx].room = random.choice(
                        state.rooms)
                elif param_idx == 1:
                    """ mutate instructor """
                    tmp_sch.classes[class_idx].instructor = \
                        random.choice(state.instructors)
                else:  # param_idx == 2
                    """ mutate timeslot """
                    tmp_sch.classes[class_idx].timeslot = \
                        random.choice(state.timeslots)

                if state.fitness(tmp_sch) < state.fitness(new_population[schedule_idx]):
                    new_population[schedule_idx] = tmp_sch

            population = new_population
        except KeyboardInterrupt:
            print("Solver stopped by user")
            break

    best_fitness = state.fitness(population[0])
    best_fit_idx = 0
    for i in range(1, len(population)):
        f = state.fitness(population[i])
        if f < best_fitness:
            best_fitness = f
            best_fit_idx = i

    return population[best_fit_idx]
