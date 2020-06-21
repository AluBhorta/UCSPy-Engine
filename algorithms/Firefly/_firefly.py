import numpy as np

from data.data import NUM_OF_ROOMS as R, NUM_OF_TIMELSOTS as T, NUM_OF_COURSES as C, NUM_OF_INSTRUCTORS as I, NUM_OF_LECS_BEING_OFFERED as L
from fitness.fitness import fitness
from data.rand_schedule_generators.grs_v1 import generate_random_schedule as grs

# get brightest firefly from population
def get_max_bright_idx(population_size, fireflies, _max_bright_idx):
    for i in range(population_size):
        if fireflies[i][1] > fireflies[_max_bright_idx][1]:
            _max_bright_idx = i

    return _max_bright_idx


def get_dist(i, j, fireflies):
    return np.abs(fireflies[i][0] - fireflies[j][0])


def get_attraction(beta, gamma, r):
    return beta * np.exp(-1 * gamma * (r**2))


def Firefly_for_UCSP(epochs=100, min_acceptable_fitness=0.5, population_size=256, gamma=0.5, beta=1, alpha=0.5):
    bounds = np.array((R, T, C, I))
    fireflies = [[None, None] for _ in range(population_size)]

    # set each firefly as [X, f(X)]
    for i in range(population_size):
        fireflies[i][0] = grs()
        fireflies[i][1] = fitness(fireflies[i][0])

    max_bright_idx = get_max_bright_idx(population_size, fireflies, 0)
    max_bright_sch = fireflies[max_bright_idx][0]

    epoch = 0
    while epoch < epochs:
        print("Epoch: %d \t max fitness: %f" %
              (epoch, fireflies[max_bright_idx][1]))

        if fireflies[max_bright_idx][1] > min_acceptable_fitness:
            return fireflies[max_bright_idx][0]

        for i in range(population_size):
            if fireflies[max_bright_idx][1] > fireflies[i][1]:
                # print(i, "before", fireflies[i][1])
                r = get_dist(i, max_bright_idx, fireflies)
                attraction = get_attraction(beta, gamma, r)
                epsilon = np.random.randn(L, 4)  # * something
                fireflies[i][0] = ((fireflies[i][0] +
                                    (attraction * (fireflies[max_bright_idx][0] - fireflies[i][0])) +
                                    (alpha * epsilon)) % bounds).astype(int)

                fireflies[i][1] = fitness(fireflies[i][0])
                # print(i, "after", fireflies[i][1])

        max_bright_idx = get_max_bright_idx(
            population_size,
            fireflies,
            max_bright_idx
        )
        max_bright_sch = fireflies[max_bright_idx][0]

        epoch += 1

    return max_bright_sch
