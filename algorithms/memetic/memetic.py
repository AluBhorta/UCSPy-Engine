import numpy as np
import random
from copy import deepcopy

from core.models import Schedule, ScheduleParam
from core.logging import UCSPLogger
from core.models.Algorithm import Algorithm
from core.models.FitnessProvider import FitnessProvider
from core.models.ScheduleGenerator import ScheduleGenerator


class MemeticAlgorithm(Algorithm):
    def __init__(
        self,
        schedule_param: ScheduleParam,
        fitness_provider: FitnessProvider,
        schedule_generator: ScheduleGenerator,
        logger: UCSPLogger,
        epochs=100,
        min_acceptable_fitness=0,
        population_size=100,
        elite_pct=10,
        mateable_pct=50,
        lcl_search_pct=10,
        lcl_search_iters=30,
    ):
        super(MemeticAlgorithm, self).__init__(
            schedule_param,
            fitness_provider,
            schedule_generator,
            logger
        )
        self.epochs = epochs
        self.min_acceptable_fitness = min_acceptable_fitness
        self.population_size = population_size
        self.elite_pct = elite_pct
        self.mateable_pct = mateable_pct
        self.lcl_search_pct = lcl_search_pct
        self.lcl_search_iters = lcl_search_iters

    def get_default_args(self, *args, **kwargs):
        return {
            "epochs": self.epochs,
            "min_acceptable_fitness": self.min_acceptable_fitness,
            "population_size": self.population_size,
            "elite_pct": self.elite_pct,
            "mateable_pct": self.mateable_pct,
            "lcl_search_pct": self.lcl_search_pct,
            "lcl_search_iters": self.lcl_search_iters,
        }

    def run(self, *args, **kwargs):
        return _memetic_algorithm(
            self.schedule_param,
            self.fitness_provider,
            self.schedule_generator,
            self.logger,
            self.epochs,
            self.min_acceptable_fitness,
            self.population_size,
            self.elite_pct,
            self.mateable_pct,
            self.lcl_search_pct,
            self.lcl_search_iters,
        )


def _memetic_algorithm(
    schedule_param: ScheduleParam,
    fitness_provider: FitnessProvider,
    schedule_generator: ScheduleGenerator,
    logger: UCSPLogger,
    epochs=100,
    min_acceptable_fitness=0,
    population_size=100,
    elite_pct=10,
    mateable_pct=50,
    lcl_search_pct=10,
    lcl_search_iters=30,
):
    # initial population
    population = [schedule_generator.generate()
                  for _ in range(population_size)]
    new_population = [None for _ in range(population_size)]

    total_classes = len(schedule_param.sections)
    logger.write(f"Generation\t\tFitness")

    for epoch in range(epochs):
        try:
            population = sorted(
                population,
                key=lambda sch: fitness_provider.fitness(sch))

            best_fitness = fitness_provider.fitness(population[0])
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

            """ Local Search using Smart Mutation """
            lcl_search_count = (lcl_search_pct * population_size)//100
            for i in range(lcl_search_count):
                schedule_idx = np.random.randint(population_size)
                class_idx = np.random.randint(total_classes)

                tmp_sch = deepcopy(new_population[schedule_idx])

                for j in range(lcl_search_iters):
                    param_idx = np.random.randint(3)

                    if param_idx == 0:
                        """ mutate room """
                        tmp_sch.classes[class_idx].room = random.choice(
                            schedule_param.rooms)
                    elif param_idx == 1:
                        """ mutate instructor """
                        tmp_sch.classes[class_idx].instructor = \
                            random.choice(schedule_param.instructors)
                    else:  # param_idx == 2
                        """ mutate timeslot """
                        tmp_sch.classes[class_idx].timeslot = \
                            random.choice(schedule_param.timeslots)

                    if fitness_provider.fitness(tmp_sch) < fitness_provider.fitness(new_population[schedule_idx]):
                        new_population[schedule_idx] = tmp_sch
                        break

            population = new_population
        except KeyboardInterrupt:
            print("Solver stopped by user")
            break

    best_fitness = fitness_provider.fitness(population[0])
    best_fit_idx = 0
    for i in range(1, len(population)):
        f = fitness_provider.fitness(population[i])
        if f < best_fitness:
            best_fitness = f
            best_fit_idx = i

    return population[best_fit_idx]
