import numpy as np
import random
from copy import deepcopy

from core.models import Schedule, ScheduleParam
from core.services.UCSPLogger import UCSPLogger
from core.models.Algorithm import Algorithm
from core.services.FitnessProvider import FitnessProvider
from core.models.ScheduleGenerator import ScheduleGenerator


class MemeticAlgorithm(Algorithm):
    def __init__(
        self,
        schedule_param: ScheduleParam,
        fitness_provider: FitnessProvider,
        schedule_generator: ScheduleGenerator,
        logger: UCSPLogger,
        epochs=100,
        min_acceptable_fitness=0.5,
        population_size=100,
        elite_pct=10,
        mateable_pct=50,
        mutable_pct=20,
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
        self.mutable_pct = mutable_pct
        self.lcl_search_pct = lcl_search_pct
        self.lcl_search_iters = lcl_search_iters

    def run(self, *args, **kwargs):
        # initial population
        population = [self.schedule_generator.generate()
                    for _ in range(self.population_size)]
        new_population = [None for _ in range(self.population_size)]

        total_classes = len(self.schedule_param.sections)
        self.logger.write(self.logger.record_start_marker)

        for epoch in range(self.epochs):
            try:
                population = sorted(
                    population,
                    key=lambda sch: self.fitness_provider.fitness(sch),
                    reverse=not self.fitness_provider.is_reverse()
                )

                best_fitness = self.fitness_provider.fitness(population[0])
                self.logger.write(f"{epoch}\t\t{best_fitness}")

                if self.fitness_provider.compare(best_fitness, self.min_acceptable_fitness):
                    return population[0]

                """ Dominance by elites """
                elite_count = (self.elite_pct * self.population_size)//100
                for i in range(elite_count):
                    new_population[i] = population[i]

                """ Crossover """
                mateable_count = (self.mateable_pct * self.population_size)//100
                siblig_index = 1 \
                    if (self.population_size - elite_count) % 2 == 0 \
                    else -1
                for i in range(elite_count, self.population_size, 2):
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
                # self.mutable_pct
                mutable_count = (self.mutable_pct * self.population_size)//100
                for i in range(mutable_count):
                    # NOTE: research on optimal choice of `schedule_idx` range
                    schedule_idx = np.random.randint(self.population_size)
                    # schedule_idx = np.random.randint(elite_count, population_size)

                    class_idx = np.random.randint(total_classes)

                    param_idx = np.random.randint(3)

                    tmp_sch = deepcopy(new_population[schedule_idx])

                    if param_idx == 0:
                        """ mutate room """
                        tmp_sch.classes[class_idx].room = random.choice(
                            self.schedule_param.rooms)
                    elif param_idx == 1:
                        """ mutate instructor """
                        tmp_sch.classes[class_idx].instructor = \
                            random.choice(self.schedule_param.instructors)
                    else:  # param_idx == 2
                        """ mutate timeslot """
                        tmp_sch.classes[class_idx].timeslot = \
                            random.choice(self.schedule_param.timeslots)

                    new_population[schedule_idx] = tmp_sch


                """ Local Search using Smart Mutation """
                lcl_search_count = (self.lcl_search_pct * self.population_size)//100
                for i in range(lcl_search_count):
                    schedule_idx = np.random.randint(self.population_size)
                    class_idx = np.random.randint(total_classes)

                    tmp_sch = deepcopy(new_population[schedule_idx])

                    for j in range(self.lcl_search_iters):
                        param_idx = np.random.randint(3)

                        if param_idx == 0:
                            """ mutate room """
                            tmp_sch.classes[class_idx].room = random.choice(
                                self.schedule_param.rooms)
                        elif param_idx == 1:
                            """ mutate instructor """
                            tmp_sch.classes[class_idx].instructor = \
                                random.choice(self.schedule_param.instructors)
                        else:  # param_idx == 2
                            """ mutate timeslot """
                            tmp_sch.classes[class_idx].timeslot = \
                                random.choice(self.schedule_param.timeslots)

                        tmp_fitness = self.fitness_provider.fitness(tmp_sch)
                        current_fitness = self.fitness_provider.fitness(new_population[schedule_idx])

                        if self.fitness_provider.compare(tmp_fitness, current_fitness):
                            new_population[schedule_idx] = tmp_sch
                            break

                population = new_population
            except KeyboardInterrupt:
                print("Solver stopped by user")
                break

        self.logger.write(self.logger.record_end_marker)
        
        best_fitness = self.fitness_provider.fitness(population[0])
        best_fit_idx = 0
        for i in range(1, len(population)):
            f = self.fitness_provider.fitness(population[i])
            if self.fitness_provider.compare(f, best_fitness):
                best_fitness = f
                best_fit_idx = i

        return population[best_fit_idx]

    def get_default_args(self, *args, **kwargs):
        return {
            "epochs": self.epochs,
            "min_acceptable_fitness": self.min_acceptable_fitness,
            "population_size": self.population_size,
            "elite_pct": self.elite_pct,
            "mateable_pct": self.mateable_pct,
            "mutable_pct": self.mutable_pct,
            "lcl_search_pct": self.lcl_search_pct,
            "lcl_search_iters": self.lcl_search_iters,
        }
