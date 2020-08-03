from pandas import read_csv
import os

from core.generators.generate_state import generate_state_from_config
from core.util import _str_to_array


def inspect_schedule(schedule_file, config_file="ucsp.config.json"):
    """ Schedule Inspector 
    
        Inspect the quality of a schedule.
    """
    def parse_num_sch_from(schedule_file):
        s = read_csv(os.path.join(os.getcwd(), schedule_file)).to_numpy()
        for i in range(len(s[:, -1])):
            s[:, -1][i] = _str_to_array(s[:, -1][i])
        return s

    _state = generate_state_from_config(config_file)

    ns = parse_num_sch_from(schedule_file)
    sch = _state.numeric_to_sch(ns)

    f_val = _state.fitness(sch, _inspect=True)
    print(f"\nFinal Fitness: {f_val}")
