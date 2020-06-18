from data.input_as_csv.parse_csv import generate_state_from_csv
from pprint import pprint 

from data.rand_schedule_generators.grs_v2 import generate_random_schedule_v2
from fitness.constraints.hard_constraints import violates_hard_constraint_1, violates_hard_constraint_2

def init():
    state = generate_state_from_csv()
    print(f"Total number of sections = {len(state.sections)}\n")
    # pprint(state)

    sch = generate_random_schedule_v2(state)
    print(":')")
    # pprint(sch.classes)

    r = violates_hard_constraint_1(sch)
    print(f"violates_hard_constraint_1? {r}")
    
    r = violates_hard_constraint_2(sch)
    print(f"violates_hard_constraint_2? {r}")


if __name__ == "__main__":
    init()
    # run_ucsp(epochs=50, population_size=128, algo="ga")
