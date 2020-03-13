
# from data.generate_random_schedule import generate_random_schedule_v2 as grs2

# from fitness.fitness import fitness

# from utility import get_algo
import numpy as np

# def run_ucsp(epochs=50, population_size=128, algo="ga", **kwargs):

#     _algo = get_algo(algo)
#     schedule = _algo(epochs=50, population_size=128, **kwargs)

#     print(schedule)  # TODO: Pretty Print the final schedule
#     print("\nFinal Fitness %f" % fitness(schedule))


def init():
    pass


if __name__ == "__main__":
    # init()
    # run_ucsp(epochs=50, population_size=128, algo="ga")

    from data.input_as_csv.parse_csv import generate_state_from_csv

    state = generate_state_from_csv()

    # print(state)
    print(len(state.sections))
