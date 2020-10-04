import numpy as np
import random
from copy import deepcopy
from typing import List

from core.models import Schedule, ScheduleParam
from core.logging import UCSPLogger
from core.models.Algorithm import Algorithm
from core.models.FitnessProvider import FitnessProvider
from core.models.ScheduleGenerator import ScheduleGenerator
from core.models.ScheduleOperator import ScheduleOperator


class Particle:
    def __init__(self, position, velocity, pbest_position):
        self.position = position
        self.velocity = velocity
        self.pbest_position = pbest_position


class ParticleSwarmOptimization(Algorithm):
    def __init__(
        self,
        schedule_param: ScheduleParam,
        fitness_provider: FitnessProvider,
        schedule_generator: ScheduleGenerator,
        logger: UCSPLogger,
        epochs=100,
        min_acceptable_fitness=0,
        population_size=5,
        w0=0.5,
        wf=0.1,
        c1=1,
        c2=1,
        vmax_pct=5
    ):
        super(ParticleSwarmOptimization, self).__init__(
            schedule_param,
            fitness_provider,
            schedule_generator,
            logger
        )
        self.epochs = epochs
        self.population_size = population_size
        self.min_acceptable_fitness = min_acceptable_fitness
        self.w0 = w0
        self.wf = wf
        self.c1 = c1
        self.c2 = c2
        self.vmax_pct = vmax_pct
        self.schedule_operator = ScheduleOperator(schedule_param)

    def run(self, *args, **kwargs):
        particles = self._generate_particles()

        weight = self.w0

        gbest_position = deepcopy(particles[0].position)
        gbest_fitness = self._get_fitness_of(gbest_position)

        for epoch in range(self.epochs):
            for particle in particles:
                current_fitness = self._get_fitness_of(particle.position)

                # NOTE: this comparision could be dynamic: > OR < depending on the type of fitness function
                # OR, a function from fitnessprovider, that takes 2 args, answering True => if left fitness is better than right fitness
                if current_fitness < self.min_acceptable_fitness:
                    return self.schedule_operator.flat_to_sch(particle.position), current_fitness

                pbest_fitness = self._get_fitness_of(particle.pbest_position)
                if current_fitness < pbest_fitness:
                    print(
                        f"current_fitness: {current_fitness}\tpbest_fitness: {pbest_fitness}")
                    particle.pbest_position = deepcopy(particle.position)

                if current_fitness < gbest_fitness:
                    print(
                        f"current_fitness: {current_fitness}\t gbest_fitness: {gbest_fitness}")
                    gbest_fitness = current_fitness
                    gbest_position = deepcopy(particle.position)

            self.logger.write(f"{epoch}\t\t{gbest_fitness}")
            weight = self._update_weight(epoch)

            for particle in particles:
                velo1 = particle.velocity

                particle.velocity = \
                    self._get_new_velocity(particle, weight, gbest_position)

                particle.position = self._get_new_position(particle)

                velo2 = particle.velocity
                # print("\nvelo1: \n", velo1)
                # print("\nvelo2: \n", velo2)
                # print("\nvelo2-velo1: \n", velo2-velo1)

        # TODO: search thru all and update gbest_position
        return self.schedule_operator.flat_to_sch(gbest_position)

    def _generate_particles(self):
        return [self._make_particle() for _ in range(self.population_size)]

    def _make_particle(self):
        position = self.schedule_generator.generate().flatten()

        velocity = []
        for _ in range((len(position)//5)):
            velocity.extend([
                0,
                0,
                np.random.randint(0, 2),
                np.random.randint(0, 2),
                np.random.randint(0, 2),
            ])
        velocity = np.array(velocity)

        return Particle(
            position,
            velocity,
            deepcopy(position)
        )

    def _get_fitness_of(self, position):
        sch = self.schedule_operator.flat_to_sch(position)
        return self.fitness_provider.fitness(sch)

    def _update_weight(self, epoch):
        dw_depoch = (self.wf-self.w0) / self.epochs
        return (dw_depoch * epoch) + self.w0

    def _get_new_velocity(self, particle: Particle, weight, gbest_position):
        v = \
            self.__velo_comp_intertia(weight, particle.velocity) + \
            self.__velo_comp_cognitive(particle.pbest_position, particle.position) + \
            self.__velo_comp_social(gbest_position, particle.position)

        return np.array([np.floor(i).astype(int) for i in v])

    def __velo_comp_intertia(self, w, V):
        return w * V

    def __velo_comp_cognitive(self, P, X):
        return self.c1 * np.random.uniform() * (P-X)

    def __velo_comp_social(self, G, X):
        return self.c2 * np.random.uniform() * (G-X)

    def _get_new_position(self, particle: Particle):
        limit = [
            len(self.schedule_param.courses),
            len(self.schedule_param.sections),
            len(self.schedule_param.instructors),
            len(self.schedule_param.rooms),
            len(self.schedule_param.timeslots),
        ] * (len(particle.position)//5)

        return (particle.position + particle.velocity) % limit

    def get_default_args(self, *args, **kwargs):
        return {
            "epochs": self.epochs,
            "population_size": self.population_size,
            "min_acceptable_fitness": self.min_acceptable_fitness,
            "w0": self.w0,
            "wf": self.wf,
            "c1": self.c1,
            "c2": self.c2,
            "vmax_pct": self.vmax_pct,
        }
