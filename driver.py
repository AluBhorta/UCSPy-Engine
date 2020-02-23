import numpy as np
# from matplotlib import pyplot as plt

from data.data import ROOMS as R, TIMESLOTS as T, COURSES as C, INSTRUCTORS as I, NUM_OF_LECS_BEING_OFFERED as L
from data.generate_random_schedule import generate_random_schedule, generate_random_schedule_v2 as grs2

from fitness.solution_encoding import encode, decode
from fitness.fitness import fitness

from algorithms.GA.ga import GA_for_UCSP
from algorithms.Memetic.memetic import Memetic_for_UCSP
from algorithms.PSO.pso import PSO_for_UCSP
from algorithms.Firefly.firefly import Firefly_for_UCSP


def print_params():
    print(
        ("\nROOMS: %d (int room_idx, str room_desc) \n" % len(R)), R)
    print(
        ("\nTIMESLOTS: %d (int timeslot_idx, str timeslot_desc) \n" % len(T)), T)
    print(
        ("\nCOURSES: %d (int course_idx, str course_desc, int num_of_lectures, int[] preferred_rooms, int[] preferred_timeslots)\n" % len(C)), C)
    print(
        ("\nINSTRUCTORS: %d (int instuctor_idx, str instuctor_desc, int[] qualified_courses, int[] available_timeslots, int[] preferred_rooms, int[] preferred_timeslots)\n" % len(I)), I)
    print("\nNUM_OF_LECS_BEING_OFFERED: \n", L)


def check_fitness(iterations=100):
    '''check fitg_best_fitnessssions '''
    counter = 0

    for i in range(iterations):
        sch = grs2()
        f = fitness(sch)
        print(f)

        if f > 0:
            counter += 1
        # print(counter)

    print("fitness(sch) > 0: %d times!" % counter)


def write_data_to_file(fname, data):
    f = open(fname, "w")
    f.write(data)
    f.close()


def bencher():
    def do_bench(epochs, poplation_size):
        results = GA_for_UCSP(population_size=poplation_size, epochs=epochs)
        fname = "results/fitness_vals/ga-results-e_%d-pop_%d.txt" % (
            epochs, poplation_size)

        # prepare data for recording: epoch vs fitness
        data = ""
        for row in results[:, :2]:
            data += str(row[0]) + "," + str(row[1]) + "\n"

        write_data_to_file(fname, data)

        print("\nFinal Fitness %f" % fitness(results[-1, 2]))

    epochs = 115
    poplation_size = 256

    for i in range(3):
        do_bench(epochs, poplation_size)
        poplation_size = poplation_size * 2


def get_decoded_schedule(sch):
    def get_dec_room(room):
        return "\tROOM - index: %d | desc: %s\n" % (room[0], room[1])

    def get_dec_timeslot(timeslot):
        return "\tTIMESLOT - index: %d | desc: %s\n" % (timeslot[0], timeslot[1])

    def get_dec_course(course):
        pr = [R[i][1] for i in course[3]]
        pt = [T[i][1] for i in course[4]]
        return "\tCOURSE - index: %d | desc: %s | num of lectures: %d | preferred rooms: %s | preferred timeslots: %s\n" % (course[0], course[1], course[2], pr, pt)

    def get_dec_instr(instr):
        qc = [C[i][1] for i in instr[2]]
        at = [T[i][1] for i in instr[3]]

        pr = [R[i][1] for i in instr[4]]
        pt = [T[i][1] for i in instr[5]]
        return "\tINSTRUCTOR - index: %d | desc: %s | qualified courses: %s | available timeslots: %s | preferred rooms: %s | preferred timeslots: %s\n" % (instr[0], instr[1], qc, at, pr, pt)

    def get_dec_lec(lec):
        _lec = ""
        _lec += get_dec_room(lec[0])
        _lec += get_dec_timeslot(lec[1])
        _lec += get_dec_course(lec[2])
        _lec += get_dec_instr(lec[3])
        return _lec

    out = "SCHEDULE\n"
    for i in range(len(sch)):
        out += "  LECTURE %d \n" % i
        out += get_dec_lec(decode(sch[i]))

    return out


def write_final_schedules(epochs=110, poplation_size=256):
    results = GA_for_UCSP(population_size=poplation_size, epochs=epochs)

    fname = "results/final_schedules/ga-de_sch-e_%d-pop_%d.txt" % (
        epochs, poplation_size)

    last2 = results[-2:, :]

    data = ""
    for row in last2:
        data += "Epoch: %d | Fitness: %f \n" % (row[0], row[1])
        data += str(get_decoded_schedule(row[2])) + "\n"

    print(last2)

    write_data_to_file(fname, data)


def main():
    '''main driver function

    tweak the parameters & comment or uncomment whichever algorithm you'd want to use.
    '''
    epochs = 50
    poplation_size = 128

    schedule = GA_for_UCSP(population_size=poplation_size, epochs=epochs)
    # schedule = Memetic_for_UCSP(population_size=poplation_size, epochs=epochs)

    # schedule = PSO_for_UCSP(epochs=epochs, total_particles=poplation_size,)
    # schedule = Firefly_for_UCSP(population_size=poplation_size, epochs=epochs,)

    print("\nFinal Schedule:\n", get_decoded_schedule(schedule))
    print("\nFinal Fitness %f" % fitness(schedule))


if __name__ == "__main__":
    print(f"NUM_OF_LECS_BEING_OFFERED: {L}\n")
    # check_fitness()
    
    main()
    
    # s = grs2()
    # print(s)
    # print(fitness(s))
    
    # print_params()
