import numpy as np

from data.data import NUM_OF_ROOMS as R, NUM_OF_TIMELSOTS as T, NUM_OF_COURSES as C, NUM_OF_INSTRUCTORS as I, NUM_OF_LECS_BEING_OFFERED as L
from fitness.fitness import fitness
from data.generate_random_schedule import generate_random_schedule


def PSO_for_UCSP(epochs=100, min_acceptable_fitness=0.5, total_particles=256, weight=0.9, c1=2, c2=2):
    particles = [[None, None, None] for _ in range(total_particles)]
    v_max = (R, T, C, I)

    # 0th index for sch, 1th index for personal_best sch, 2nd for velocity
    # [X_current, P_best, Velocity]
    for i in range(total_particles):
        particles[i][0] = generate_random_schedule()
        particles[i][1] = particles[i][0]
        particles[i][2] = np.random.randint(
            1,
            min(v_max),
            size=(L, 4)
        )

    global_best_sch = particles[0][0]
    global_best_fitness = 0

    epoch = 0
    while epoch < epochs:
        for i in range(len(particles)):
            current_fitness = fitness(particles[i][0])
            if current_fitness > min_acceptable_fitness:
                return particles[i][0]

            p_best_fitness = fitness(particles[i][1])
            if current_fitness > p_best_fitness:
                particles[i][1] = particles[i][0]

        global_best_fitness = fitness(global_best_sch)
        for i in range(len(particles)):
            if p_best_fitness > global_best_fitness:
                global_best_sch = particles[i][1]

        # TODO update weight

        for i in range(len(particles)):
            # update velocity
            particles[i][2] = (weight * particles[i][2]) + \
                (c1 * np.random.uniform() * (particles[i][1] - particles[i][0])) + \
                ((c2 * np.random.uniform() *
                  (global_best_sch - particles[i][0])))

            # print("velocity %d:\n" % i, particles[i][2])
            # particles[i][2] %= v_max

            # update current position i.e. current schedule
            particles[i][0] = particles[i][0] + particles[i][2]

        epoch += 1

    return global_best_sch
