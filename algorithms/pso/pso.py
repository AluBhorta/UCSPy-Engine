
import numpy as np
import random
from copy import deepcopy
from pprint import pprint
import math

from core.schedule_generators.grs import generate_random_schedule as grs
from core.fitness import fitness
from core.models import StateManager, Schedule


def particle_swarm_optimization(
    state: StateManager,
    epochs=100,
    min_acceptable_fitness=1,
    population_size=20,
    w0=0.8, wf=0.2, c1=1, c2=2, vmax_pct=5
):
    def c_velo(w, V): return w * V
    def c_indi(P, X): return c1 * np.random.uniform() * (P-X)
    def c_glob(G, X): return c2 * np.random.uniform() * (G-X)

    def update_w(epoch):
        dw_depoch = (wf-w0) / epochs
        return (dw_depoch * epoch) + w0

    lim_c = len(state.courses)
    lim_s = len(state.sections)
    lim_r = len(state.rooms)
    lim_i = len(state.instructors)
    lim_ts = len(state.timeslots)

    vmax_lim = np.ceil(
        np.array([1, 1, lim_i, lim_r, lim_ts]) * (vmax_pct/100)
    ).astype(int)

    part_max_lim = np.array([lim_c, lim_s, lim_i, lim_r, lim_ts])

    particles = [[None, None, None] for _ in range(population_size)]

    # each particle consists of [X_current, P_best, Velocity]
    for i in range(population_size):
        particles[i][0] = grs(state).get_numeric_repr()
        particles[i][1] = deepcopy(particles[i][0])
        particles[i][2] = particles[i][0] % vmax_lim

    weight = w0  # current weight

    g_best_idx = 0
    g_best_fitness = 0.0

    for epoch in range(epochs):
        for i in range(len(particles)):
            current_fitness = fitness(
                state.numeric_to_sch(particles[i][0])
            )
            if current_fitness > min_acceptable_fitness:
                return particles[i][0]

            p_best_fitness = fitness(
                state.numeric_to_sch(particles[i][1])
            )
            # print(current_fitness, p_best_fitness)
            if current_fitness > p_best_fitness:
                print(f"nice cf: {current_fitness} \tpf: {p_best_fitness}")
                particles[i][1] = deepcopy(particles[i][0])
                p_best_fitness = current_fitness

            if p_best_fitness > g_best_fitness:
                print(f"GG! pf: {p_best_fitness} \tgf: {g_best_fitness}")
                g_best_fitness = p_best_fitness
                g_best_idx = i

        print("Epoch: %d \t G_BEST fitness: %f" % (epoch, g_best_fitness))
        weight = update_w(epoch)

        for i in range(len(particles)):
            particles[i][2] = c_velo(weight, particles[i][2]) + \
                c_indi(particles[i][1], particles[i][0]) + \
                c_glob(particles[g_best_idx][1], particles[i][0])

            particles[i][2] = particles[i][2] % vmax_lim  # limit

            a = particles[i][2][:, :-1].astype(int)
            b = particles[i][2][:, -1]

            o = []
            for j in range(len(b)):
                o.append([*a[j], b[j].astype(int)])
            particles[i][2] = np.array(o)

            particles[i][0] = (
                particles[i][0] + particles[i][2]
            ) % part_max_lim

        # print(particles[0][2][10:30])

    final_sch = state.numeric_to_sch(particles[g_best_idx][1])
    print(f"Final fitness: {fitness(final_sch)}")

    return final_sch
