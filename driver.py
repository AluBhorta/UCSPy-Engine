from data.input_as_csv.parse_csv import generate_state_from_csv
from pprint import pprint

from data.rand_schedule_generators.grs_v2 import generate_random_schedule_v2

from fitness.constraints.hard_constraints import violates_hard_constraint_1, violates_hard_constraint_2
from fitness.constraints.soft_constraints import SOFT_CONSTRAINTS
from fitness.fitness import fitness


def init():
    state = generate_state_from_csv()

    sch = generate_random_schedule_v2(state)
    print(fitness(sch))
    
    # return print(sch)
    # for penalty in SOFT_CONSTRAINTS:
    #     r = penalty(sch)
    #     print(r)

    


if __name__ == "__main__":
    init()
    # run_ucsp(epochs=50, population_size=128, algo="ga")
