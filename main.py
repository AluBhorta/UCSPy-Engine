from pprint import pprint
import numpy as np

# from core.runner import run_ucsp
from core.parsers.parse_csv import generate_state_from_csv
from core.schedule_generators.grs import generate_random_schedule as grs
from core.fitness import fitness
from algorithms.genetic.ga import genetic_algorithm
from algorithms.pso.pso import particle_swarm_optimization

state = generate_state_from_csv()


def run_pso():
    sch = particle_swarm_optimization(state)
    # return print(sch)


def test():

    pass


if __name__ == "__main__":
    # test()
    run_pso()

    pass
