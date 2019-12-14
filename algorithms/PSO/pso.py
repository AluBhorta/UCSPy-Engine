import numpy as np

from data.data import NUM_OF_ROOMS as R, NUM_OF_TIMELSOTS as T, NUM_OF_COURSES as C, NUM_OF_INSTRUCTORS as I, NUM_OF_LECS_BEING_OFFERED as L
from fitness.fitness import fitness
from data.generate_random_schedule import generate_random_schedule


def PSO_for_UCSP(epochs=100, total_particles=256, min_acceptable_fitness=0.5, w0=0.9, wf=0.2, c1=2, c2=2):
    '''
    ISSUE: Does not improve fitness after first epoch. (TODO) find out why
    '''
    particles = [[None, None, None] for _ in range(total_particles)]
    v_max = np.array((R, T, C, I))

    # each particle consists of [X_current, P_best, Velocity]
    for i in range(total_particles):
        particles[i][0] = generate_random_schedule()
        particles[i][1] = particles[i][0]
        particles[i][2] = np.random.randn(L, 4) % v_max

    # each components of the velocity update equation
    def c_velo(w, V): return w * V
    def c_indi(P, X): return c1 * np.random.uniform() * (P-X)
    def c_glob(G, X): return c2 * np.random.uniform() * (G-X)

    # current weight
    weight = w0
    # the gradient
    dw_depoch = (wf-w0) / epochs
    # w(x) = mx + c
    def update_w(epoch): return (dw_depoch * epoch) + w0

    g_best_idx = 0
    g_best_fitness = 0.0

    epoch = 0
    while epoch < epochs:
        for i in range(len(particles)):
            current_fitness = fitness(particles[i][0])
            if current_fitness > min_acceptable_fitness:
                return particles[i][0]

            p_best_fitness = fitness(particles[i][1])
            if current_fitness > p_best_fitness:
                particles[i][1] = particles[i][0]
                p_best_fitness = current_fitness

            # g_best_fitness = fitness(particles[g_best_idx][1])
            if p_best_fitness > g_best_fitness:
                # print("Bingo!")
                # print("i:%d f(X):%f \tf(P):%f \tf(G):%f" %
                #       (i, current_fitness, p_best_fitness, g_best_fitness))
                g_best_fitness = p_best_fitness
                g_best_idx = i

        print("Epoch: %d \t glob_fit: %f" % (epoch, g_best_fitness))
        weight = update_w(epoch)

        for i in range(len(particles)):
            # update velocity
            particles[i][2] = c_velo(weight, particles[i][2]) + \
                c_indi(particles[i][1], particles[i][0]) + \
                c_glob(particles[g_best_idx][1], particles[i][0])

            # update current position i.e. current schedule
            particles[i][0] = (
                np.floor(particles[i][0] + particles[i][2]) % v_max).astype(int)

        epoch += 1

    return particles[g_best_idx][1]
