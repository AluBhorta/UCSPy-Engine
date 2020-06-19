from pprint import pprint
import random


from data.input_as_csv.parse_csv import generate_state_from_csv
from data.rand_schedule_generators.grs_v2 import generate_random_schedule_v2 as grs
from fitness.fitness import fitness
from algorithms.GA.ga_v2 import genetic_algorithm_v2

state = generate_state_from_csv()


def init():
    sch = grs(state)
    print(sch)

    # sch = genetic_algorithm_v2(state)
    # f = fitness(sch)
    # print(f"Final fitness: {f}")

    pass


if __name__ == "__main__":
    init()

    # run_ucsp(epochs=50, population_size=128, algo="ga")
