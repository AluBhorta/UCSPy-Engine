from data.input_as_csv.parse_csv import generate_state_from_csv
from pprint import pprint

from data.rand_schedule_generators.grs_v2 import generate_random_schedule_v2
from fitness.fitness import fitness


def init():
    state = generate_state_from_csv()

    for _ in range(100):
        sch = generate_random_schedule_v2(state)
        f = fitness(sch)
        print(f)


if __name__ == "__main__":
    init()
    # run_ucsp(epochs=50, population_size=128, algo="ga")
